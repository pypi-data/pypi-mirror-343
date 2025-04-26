"""
DDNet MCP服务器的测试文件
"""
import pytest
from fastmcp import Client
from ddnet_mcpserver.server import mcp

@pytest.mark.asyncio
async def test_add_tool():
    """测试加法工具"""
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 5, "b": 7})
        assert result.content[0].text == "12"

@pytest.mark.asyncio
async def test_greeting_resource():
    """测试问候资源"""
    async with Client(mcp) as client:
        result = await client.read_resource("greeting://测试用户")
        assert "Hello, 测试用户" in result.content[0].text 