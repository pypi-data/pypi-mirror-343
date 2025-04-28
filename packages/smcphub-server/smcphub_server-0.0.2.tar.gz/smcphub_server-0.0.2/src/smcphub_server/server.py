from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from httpx import AsyncClient, HTTPError
import time
import os
import ast
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class SmcphubServer:
    tools: [Tool]

    def __init__(self):
        self.endpoint = 'https://www.smcphub.com'
        if os.getenv('APP_ENV', 'production') == 'dev':
            self.endpoint = 'http://localhost:5000'

    def getAuthHeaders(self):
        api_key = os.getenv('SMCPHUB_API_KEY', '')
        return {
            'x-api-key': api_key,
            'x-timestamp': str(int(time.time() * 1000)),
        }

    async def init(self):
        self.tools = await self.loadAvailableServers()
        await self.serve();

    async def loadAvailableServers(self):
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    self.endpoint + "/mcp/service/list",
                    follow_redirects=True,
                    headers={"Content-Type": "application/json", **self.getAuthHeaders()},
                    timeout=30,
                )
            except HTTPError as e:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to load services: {e!r}"))
        
            if response.status_code >= 400:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to load servers - status code {response.status_code}",
                ))

            services = response.json() or []
        
        # check if length is larger than 0
        tools = []
        if len(services) > 0:
            for service in services:
                serviceTools = service['tools']
                for serviceTool in serviceTools:
                    tools.append(Tool(
                        name=serviceTool['name'],
                        description=serviceTool['description'],
                        inputSchema=serviceTool['input_schema'],
                    ));

        return tools

    async def callTool(self, service, name, args):
        service_id = service['id'] or 0
        exec_env = service['exec_env'] or 'remote'
        package_name = service['package_name'] or ''
        settings = service['settings'] or {}

        async with AsyncClient() as client:
            try:
                response = await client.post(
                    self.endpoint + "/mcp/tool/call",
                    follow_redirects=True,
                    headers={"Content-Type": "application/json", **self.getAuthHeaders()},
                    timeout=30,
                    json={'service_id': service_id, 'name': name, 'args': args }
                )
            except HTTPError as e:
                raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Failed to load services: {e!r}"))
        
            if response.status_code >= 400:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to load servers - status code {response.status_code}",
                ))

            items = response.json() or []

        return items

    async def serve(self) -> None:
        """Run the Smcphub MCP server.

        Args:
        """
        server = Server("smcphub-server")

        @server.list_tools()
        async def list_tools() -> list[Tool]:
            return self.tools

        @server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            return [
                
            ]

        @server.call_tool()
        async def call_tool(name, arguments: dict) -> list[TextContent]:
            self.callTool(name, arguments);
            return [TextContent(type="text", text=f"{prefix}Contents of {url}:\n{content}")]

        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, options, raise_exceptions=True)