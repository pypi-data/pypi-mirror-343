# server.py
from fastmcp import FastMCP
import logging
import signal
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("FastMCP-Server")

# 在现有日志配置下方添加
# 添加文件日志处理
file_handler = logging.FileHandler('ddnet_mcp_server.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# 创建MCP服务器
mcp = FastMCP("Demo")

# 添加一个加法工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    logger.info(f"执行加法: {a} + {b}")
    return a + b

# 添加一个动态问候资源
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    logger.info(f"获取问候: {name}")
    return f"Hello, {name}!"

# 处理终止信号
def signal_handler(sig, frame):
    logger.info("接收到终止信号，正在关闭服务器...")
    # 这里可以添加任何需要的清理代码
    sys.exit(0)

# 注册信号处理程序
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    logger.info("服务器正在启动...")
    try:
        logger.info("服务器正在运行，按Ctrl+C可以停止服务器...")
        # 尝试明确指定transport参数
        mcp.run(transport="stdio")  # 使用标准输入/输出作为传输方式
    except Exception as e:
        logger.error(f"服务器出错: {e}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        logger.info("服务器已关闭")