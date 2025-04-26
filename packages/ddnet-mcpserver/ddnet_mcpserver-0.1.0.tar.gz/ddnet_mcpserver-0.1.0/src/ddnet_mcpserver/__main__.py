"""
使包可直接执行的入口点
"""
import sys
import time
from .server import mcp, logger

def main():
    """主入口函数"""
    print("DDNet MCP Server 正在启动...")
    
    try:
        print("准备运行服务器...")
        # 添加调试延迟
        print("5秒后启动服务器，按Ctrl+C可取消...")
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)
            
        print("正在启动服务器...")
        # 打印服务器信息
        print(f"服务器名称: {mcp.name}")
        try:
            print(f"服务器设置: {mcp.settings}")
        except:
            print("无法获取服务器设置")
        
        # 运行服务器
        print("服务器启动中，这可能需要一段时间...")
        mcp.run(transport="stdio")
        # 如果运行到这里，说明mcp.run()没有阻塞
        print("警告：服务器可能立即退出了！")
        
    except KeyboardInterrupt:
        print("\n接收到键盘中断，取消启动...")
    except Exception as e:
        print(f"服务器错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        print("程序结束")
    
    # 保持控制台开启
    input("按Enter键退出...")
    return 0

if __name__ == "__main__":
    sys.exit(main())