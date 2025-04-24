from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Prompt

class TwinicServer:
    def __init__(self, name: str):
        self.server = Server(name)

    def add_prompt(self, name: str, description: str, arguments: list):
        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            return [Prompt(name=name, description=description, arguments=arguments)]

    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)
