import asyncio
import json
import unittest
from importlib.util import find_spec
from tests.TestCase import TestCase
from app.Inspire import Inspire


@unittest.skipUnless(find_spec('fastmcp'), 'fastmcp is not installed')
class TestMcpServer(TestCase):
    def mcp(self, request):
        """
        Connect an in-memory FastMCP client to mcpserver.py (no subprocess, no network),
        run `request(client)` and return its result.
        """
        from fastmcp import Client
        from mcpserver import mcp

        async def run():
            async with Client(mcp) as client:
                return await request(client)

        return asyncio.run(run())

    def test_server_exposes_tools_resources_and_prompts(self):
        tools = self.mcp(lambda client: client.list_tools())
        resources = self.mcp(lambda client: client.list_resources())
        prompts = self.mcp(lambda client: client.list_prompts())

        self.assertEqual(['inspire'], [tool.name for tool in tools])
        self.assertEqual(['quotes://all'], [str(resource.uri) for resource in resources])
        self.assertEqual(['motivate'], [prompt.name for prompt in prompts])

    def test_inspire_tool(self):
        quote = self.fake.sentence()

        # Override any App service before calling the server, then restore it
        self.app.inspiring.override(Inspire([quote]))
        self.addCleanup(self.app.inspiring.reset_override)

        result = self.mcp(lambda client: client.call_tool('inspire', {}))

        self.assertFalse(result.is_error)
        self.assertEqual(quote, result.data)

    def test_quotes_resource(self):
        contents = self.mcp(lambda client: client.read_resource('quotes://all'))

        self.assertEqual(
            self.app.config.inspiring.quotes(),
            json.loads(contents[0].text)
        )

    def test_motivate_prompt(self):
        topic = self.fake.word()

        result = self.mcp(lambda client: client.get_prompt('motivate', {'topic': topic}))

        self.assertIn(topic, result.messages[0].content.text)


if __name__ == '__main__':
    unittest.main()
