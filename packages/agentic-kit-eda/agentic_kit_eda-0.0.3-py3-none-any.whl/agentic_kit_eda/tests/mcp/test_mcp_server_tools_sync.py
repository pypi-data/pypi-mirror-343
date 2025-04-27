import asyncio
import unittest

from agentic_kit_eda.toolkit.mcp_toolkit import McpToolkit


class MyTestCase(unittest.TestCase):
    def test_create_mcp_toolkit(self):
        MCP_SERVER_SSE_URL = "http://221.229.0.177:8881/mcp/ds"
        tk = McpToolkit.create(mcp_server_url=MCP_SERVER_SSE_URL, name='ds', description='ds tools')
        print(tk)

        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
