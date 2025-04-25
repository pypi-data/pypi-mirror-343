from mcp.server.fastmcp import FastMCP
from pydantic import Field

# 创建FastMCP实例
mcp = FastMCP("stdio Demo")

# 增加一个工具，a+b等于几
@mcp.tool()
def add(a: int=Field(description="第一个参数"), b: int=Field(description="第二个参数")) -> dict:
    return {
            "contents": [{
                "type": "text", 
                "text": f"{a+b}"
            }]
        }


# 定义 main 函数作为入口点
def main():
    print("Starting my SSE HTTP Custom Param Server...")
    mcp.run()

# 如果直接运行脚本，也调用 main 函数
if __name__ == '__main__':
    main()