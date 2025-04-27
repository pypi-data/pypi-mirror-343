import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client

from .flat_toolkit import FlatToolkit


class McpToolkit(FlatToolkit):

    def dump(self):
        print('----dump McpToolkit----')
        super().dump()

    @classmethod
    def create(cls, mcp_server_url: str, name: str, description: str, **kwargs):
        tk = asyncio.run(cls.acreate(mcp_server_url=mcp_server_url, name=name, description=description))
        return tk

    @classmethod
    async def acreate(cls, mcp_server_url: str, name: str, description: str, **kwargs):
        tk = cls(name=name, description=description)
        async with sse_client(mcp_server_url) as (read, write):
            print('MCP server连接成功')
            async with ClientSession(read, write) as session:
                # 初始化连接
                print('MCP server session已建立')
                await session.initialize()
                print('MCP server session已初始化')

                tools = await load_mcp_tools(session)
                for tool in tools:
                    tk.add_tool(tool)
        return tk
