# Standard library imports
import logging
import os
import sys
from contextlib import AsyncExitStack, asynccontextmanager
from typing import (
    Any,
    Awaitable,
    Callable,
    cast,
    NoReturn,
    NotRequired,
    TextIO,
    TypeAlias,
    TypedDict,
)
from urllib.parse import urlparse

# Third-party imports
try:
    from anyio.streams.memory import (
        MemoryObjectReceiveStream,
        MemoryObjectSendStream,
    )
    from jsonschema_pydantic import jsonschema_to_pydantic  # type: ignore
    from langchain_core.tools import BaseTool, ToolException
    from mcp import ClientSession
    from mcp.client.sse import sse_client
    from mcp.client.stdio import stdio_client, StdioServerParameters
    from mcp.client.websocket import websocket_client
    import mcp.types as mcp_types
    from pydantic import BaseModel
    # from pydantic_core import to_json
except ImportError as e:
    print(f"\nError: Required package not found: {e}")
    print("Please ensure all required packages are installed\n")
    sys.exit(1)


class McpServerCommandBasedConfig(TypedDict):
    """Configuration for an MCP server launched via command line.

    This configuration is used for local MCP servers that are started as child
    processes using the stdio client. It defines the command to run, optional
    arguments, environment variables, working directory, and error logging
    options.

    Attributes:
        command: The executable command to run (e.g., "npx", "uvx", "python").
        args: Optional list of command-line arguments to pass to the command.
        env: Optional dictionary of environment variables to set for the
                process.
        cwd: Optional working directory where the command will be executed.
        errlog: Optional file-like object for redirecting the server's stderr
                output.

    Example:
        {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "env": {"NODE_ENV": "production"},
            "cwd": "/path/to/working/directory",
            "errlog": open("server.log", "w")
        }
    """
    command: str
    args: NotRequired[list[str] | None]
    env: NotRequired[dict[str, str] | None]
    cwd: NotRequired[str | None]
    errlog: NotRequired[TextIO | None]


class McpServerUrlBasedConfig(TypedDict):
    """Configuration for a remote MCP server accessed via URL.

    This configuration is used for remote MCP servers that are accessed via
    HTTP/HTTPS (Server-Sent Events) or WebSocket connections. It defines the
    URL to connect to and optional HTTP headers for authentication.

    Attributes:
        url: The URL of the remote MCP server. For SSE servers,
                use http:// or https:// prefix. For WebSocket servers,
                use ws:// or wss:// prefix.
        headers: Optional dictionary of HTTP headers to include in the request,
                typically used for authentication (e.g., bearer tokens).

    Example for SSE server:
        {
            "url": "https://example.com/mcp/sse",
            "headers": {"Authorization": "Bearer token123"}
        }

    Example for WebSocket server:
        {
            "url": "wss://example.com/mcp/ws"
        }
    """
    url: str
    headers: NotRequired[dict[str, str] | None]


# Type for a single MCP server configuration, which can be either
# command-based or URL-based.
SingleMcpServerConfig = McpServerCommandBasedConfig | McpServerUrlBasedConfig
"""Configuration for a single MCP server, either command-based or URL-based.

This type represents the configuration for a single MCP server, which can
be either:
1. A local server launched via command line (McpServerCommandBasedConfig)
2. A remote server accessed via URL (McpServerUrlBasedConfig)

The type is determined by the presence of either the "command" key
(for command-based) or the "url" key (for URL-based).
"""

# Configuration dictionary for multiple MCP servers
McpServersConfig = dict[str, SingleMcpServerConfig]
"""Configuration dictionary for multiple MCP servers.

A dictionary mapping server names (as strings) to their respective
configurations. Each server name acts as a logical identifier used for logging
and debugging. The configuration for each server can be either command-based
or URL-based.

Example:
    {
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
        },
        "fetch": {
            "command": "uvx",
            "args": ["mcp-server-fetch"]
        },
        "remote-server": {
            "url": "https://example.com/mcp/sse",
            "headers": {"Authorization": "Bearer token123"}
        }
    }
"""


def fix_schema(schema: dict) -> dict:
    """Converts JSON Schema "type": ["string", "null"] to "anyOf" format.

    Args:
        schema: A JSON schema dictionary

    Returns:
        Modified schema with converted type formats
    """
    if isinstance(schema, dict):
        if "type" in schema and isinstance(schema["type"], list):
            schema["anyOf"] = [{"type": t} for t in schema["type"]]
            del schema["type"]  # Remove "type" and standardize to "anyOf"
        for key, value in schema.items():
            schema[key] = fix_schema(value)  # Apply recursively
    return schema


# Type alias for the bidirectional communication channels with the MCP server
# FIXME: not defined in mcp.types, really?
Transport: TypeAlias = tuple[
    MemoryObjectReceiveStream[mcp_types.JSONRPCMessage | Exception],
    MemoryObjectSendStream[mcp_types.JSONRPCMessage]
]


async def spawn_mcp_server_and_get_transport(
    server_name: str,
    server_config: SingleMcpServerConfig,
    exit_stack: AsyncExitStack,
    logger: logging.Logger = logging.getLogger(__name__)
) -> Transport:
    """Spawns an MCP server process and establishes communication channels.

    Args:
        server_name: Server instance name to use for better logging
        server_config: Configuration dictionary for server setup
        exit_stack: Context manager for cleanup handling
        logger: Logger instance for debugging and monitoring

    Returns:
        A tuple of receive and send streams for server communication

    Raises:
        Exception: If server spawning fails
    """
    try:
        logger.info(f'MCP server "{server_name}": '
                    f"initializing with: {server_config}")

        url_str = str(server_config.get("url"))  # None becomes "None"
        headers = (cast(McpServerUrlBasedConfig, server_config)
                   .get("headers", None))
        # no exception thrown even for a malformed URL
        url_scheme = urlparse(url_str).scheme

        if url_scheme in ("http", "https"):
            transport = await exit_stack.enter_async_context(
                sse_client(url_str, headers=headers)
            )

        elif url_scheme in ("ws", "wss"):
            transport = await exit_stack.enter_async_context(
                websocket_client(url_str)
            )

        else:
            # NOTE: `uv` and `npx` seem to require PATH to be set.
            # To avoid confusion, it was decided to automatically append it
            # to the env if not explicitly set by the config.
            config = cast(McpServerCommandBasedConfig, server_config)
            # env = config.get("env", {}) does't work since it can yield None
            env_val = config.get("env")
            env = {} if env_val is None else dict(env_val)
            if "PATH" not in env:
                env["PATH"] = os.environ.get("PATH", "")

            # Use stdio client for commands
            # args = config.get("args", []) does't work since it can yield None
            args_val = config.get("args")
            args = [] if args_val is None else list(args_val)
            server_parameters = StdioServerParameters(
                command=config.get("command", ""),
                args=args,
                env=env,
                cwd=config.get("cwd", None)
            )

            # Initialize stdio client and register it with exit stack for
            # cleanup
            # NOTE: Why the key name `errlog` for `server_config` was chosen:
            # Unlike TypeScript SDK's `StdioServerParameters`, the Python
            # SDK's `StdioServerParameters` doesn't include `stderr: int`.
            # Instead, it calls `stdio_client()` with a separate argument
            # `errlog: TextIO`.  I once included `stderr: int` for
            # compatibility with the TypeScript version, but decided to
            # follow the Python SDK more closely.
            errlog_val = (cast(McpServerCommandBasedConfig, server_config)
                          .get("errlog"))
            kwargs = {"errlog": errlog_val} if errlog_val is not None else {}
            transport = await exit_stack.enter_async_context(
                stdio_client(server_parameters, **kwargs)
            )
    except Exception as e:
        logger.error(f"Error spawning MCP server: {str(e)}")
        raise

    return transport


async def get_mcp_server_tools(
    server_name: str,
    transport: Transport,
    exit_stack: AsyncExitStack,
    logger: logging.Logger = logging.getLogger(__name__)
) -> list[BaseTool]:
    """Retrieves and converts MCP server tools to LangChain format.

    Args:
        server_name: Server instance name to use for better logging
        transport: Communication channels tuple
        exit_stack: Context manager for cleanup handling
        logger: Logger instance for debugging and monitoring

    Returns:
        List of LangChain tools converted from MCP tools

    Raises:
        Exception: If tool conversion fails
    """
    try:
        read, write = transport

        # Use an intermediate `asynccontextmanager` to log the cleanup message
        @asynccontextmanager
        async def log_before_aexit(context_manager, message):
            """Helper context manager that logs before cleanup"""
            yield await context_manager.__aenter__()
            try:
                logger.info(message)
            finally:
                await context_manager.__aexit__(None, None, None)

        # Initialize client session with cleanup logging
        session = await exit_stack.enter_async_context(
            log_before_aexit(
                ClientSession(read, write),
                f'MCP server "{server_name}": session closed'
            )
        )

        await session.initialize()
        logger.info(f'MCP server "{server_name}": connected')

        # Get MCP tools
        tools_response = await session.list_tools()

        # Wrap MCP tools into LangChain tools
        langchain_tools: list[BaseTool] = []
        for tool in tools_response.tools:

            # Define adapter class to convert MCP tool to LangChain format
            class McpToLangChainAdapter(BaseTool):
                name: str = tool.name or "NO NAME"
                description: str = tool.description or ""
                # Convert JSON schema to Pydantic model for argument validation
                args_schema: type[BaseModel] = jsonschema_to_pydantic(
                    fix_schema(tool.inputSchema)  # Apply schema conversion
                )
                session: ClientSession | None = None

                def _run(self, **kwargs: Any) -> NoReturn:
                    raise NotImplementedError(
                        "MCP tools only support async operations"
                    )

                async def _arun(self, **kwargs: Any) -> Any:
                    """Asynchronously executes the tool with given arguments.

                    Logs input/output and handles errors.

                    Args:
                        **kwargs: Arguments to be passed to the MCP tool

                    Returns:
                        Formatted response from the MCP tool as a string

                    Raises:
                        ToolException: If the tool execution fails
                    """
                    logger.info(f'MCP tool "{server_name}"/"{tool.name}" '
                                f"received input: {kwargs}")

                    try:
                        result = await session.call_tool(self.name, kwargs)

                        if hasattr(result, "isError") and result.isError:
                            raise ToolException(
                                f"Tool execution failed: {result.content}"
                            )

                        if not hasattr(result, "content"):
                            return str(result)

                        # The return type of `BaseTool`'s `arun` is `str`.
                        try:
                            result_content_text = "\n\n".join(
                                item.text
                                for item in result.content
                                if isinstance(item, mcp_types.TextContent)
                            )
                            # text_items = [
                            #     item
                            #     for item in result.content
                            #     if isinstance(item, mcp_types.TextContent)
                            # ]
                            # result_content_text =to_json(text_items).decode()

                        except KeyError as e:
                            result_content_text = (
                                f"Error in parsing result.content: {str(e)}; "
                                f"contents: {repr(result.content)}"
                            )

                        # Log rough result size for monitoring
                        size = len(result_content_text.encode())
                        logger.info(f'MCP tool "{server_name}"/"{tool.name}" '
                                    f"received result (size: {size})")

                        # If no text content, return a clear message
                        # describing the situation.
                        result_content_text = (
                            result_content_text or
                            "No text content available in response"
                        )

                        return result_content_text

                    except Exception as e:
                        logger.warn(
                            f'MCP tool "{server_name}"/"{tool.name}" '
                            f"caused error:  {str(e)}"
                        )
                        if self.handle_tool_error:
                            return f"Error executing MCP tool: {str(e)}"
                        raise

            langchain_tools.append(McpToLangChainAdapter())

        # Log available tools for debugging
        logger.info(f'MCP server "{server_name}": {len(langchain_tools)} '
                    f"tool(s) available:")
        for tool in langchain_tools:
            logger.info(f"- {tool.name}")
    except Exception as e:
        logger.error(f"Error getting MCP tools: {str(e)}")
        raise

    return langchain_tools


# A very simple pre-configured logger for fallback
def init_logger() -> logging.Logger:
    """Creates a simple pre-configured logger.

    Returns:
        A configured Logger instance
    """
    logging.basicConfig(
        level=logging.INFO,  # logging.DEBUG,
        format="\x1b[90m[%(levelname)s]\x1b[0m %(message)s"
    )
    return logging.getLogger()


# Type hint for cleanup function
McpServerCleanupFn = Callable[[], Awaitable[None]]
"""Type for the async cleanup function returned by
    convert_mcp_to_langchain_tools.

This represents an asynchronous function that takes no arguments and returns
nothing. It's used to properly shut down all MCP server connections and clean
up resources when the tools are no longer needed.

Example usage:
    tools, cleanup = await convert_mcp_to_langchain_tools(server_configs)
    # Use tools...
    await cleanup()  # Clean up resources when done
"""


async def convert_mcp_to_langchain_tools(
    server_configs: McpServersConfig,
    logger: logging.Logger | None = None
) -> tuple[list[BaseTool], McpServerCleanupFn]:
    """Initialize multiple MCP servers and convert their tools to
    LangChain format.

    This async function manages parallel initialization of multiple MCP
    servers, converts their tools to LangChain format, and provides a cleanup
    mechanism. It orchestrates the full lifecycle of multiple servers.

    Args:
        server_configs: Dictionary mapping server names to their
            configurations, where each configuration contains command, args,
            and env settings
        logger: Logger instance to use for logging events and errors.
            If None, uses module logger with fallback to a pre-configured
            logger when no root handlers exist.

    Returns:
        A tuple containing:

        * List of converted LangChain tools from all servers
        * Async cleanup function to properly shutdown all server connections

    Example:

        server_configs = {
            "fetch": {
                "command": "uvx", "args": ["mcp-server-fetch"]
            },
            "weather": {
                "command": "npx", "args": ["-y","@h1deya/mcp-server-weather"]
            }
        }

        tools, cleanup = await convert_mcp_to_langchain_tools(server_configs)

        # Use tools...

        await cleanup()
    """

    if logger is None:
        logger = logging.getLogger(__name__)
        # Check if the root logger has handlers configured
        if not logging.root.handlers and not logger.handlers:
            # No logging configured, use a simple pre-configured logger
            logger = init_logger()

    # Initialize AsyncExitStack for managing multiple server lifecycles
    transports: list[Transport] = []
    async_exit_stack = AsyncExitStack()

    # Spawn all MCP servers concurrently
    for server_name, server_config in server_configs.items():
        # NOTE: the following `await` only blocks until the server subprocess
        # is spawned, i.e. after returning from the `await`, the spawned
        # subprocess starts its initialization independently of (so in
        # parallel with) the Python execution of the following lines.
        transport = await spawn_mcp_server_and_get_transport(
            server_name,
            server_config,
            async_exit_stack,
            logger
        )
        transports.append(transport)

    # Convert tools from each server to LangChain format
    langchain_tools: list[BaseTool] = []
    for (server_name, server_config), transport in zip(
        server_configs.items(),
        transports,
        strict=True
    ):
        tools = await get_mcp_server_tools(
            server_name,
            transport,
            async_exit_stack,
            logger
        )
        langchain_tools.extend(tools)

    # Define a cleanup function to properly shut down all servers
    async def mcp_cleanup() -> None:
        """Closes all server connections and cleans up resources."""
        await async_exit_stack.aclose()

    # Log summary of initialized tools
    logger.info(f"MCP servers initialized: {len(langchain_tools)} tool(s) "
                f"available in total")
    for tool in langchain_tools:
        logger.debug(f"- {tool.name}")

    return langchain_tools, mcp_cleanup
