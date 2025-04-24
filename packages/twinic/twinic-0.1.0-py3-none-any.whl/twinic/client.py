from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.models import StdioServerParameters

class TwinicClient:
    def __init__(self, server_command: str, server_args: list = []):
        self.server_params = StdioServerParameters(command=server_command, args=server_args)

    async def interact(self):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await session.list_prompts()
    ...
