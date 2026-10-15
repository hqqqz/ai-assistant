"""
自研 MCP Server：为 Agent 提供文件读写 / 时间查询工具。
通过 MCP 标准协议（stdio）暴露，可被任何 MCP Host（LangChain Agent、Cline 等）复用。
"""
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("assistant-tools")


@mcp.tool
def save_to_file(filename: str, content: str) -> str:
    """保存文本内容到指定文件。当用户要求把结果/报告保存、写入文件时调用。"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"已保存到 {filename}"
    except Exception as e:
        return f"保存失败: {e}"


@mcp.tool
def read_file(filename: str) -> str:
    """读取本地文件内容。当用户要求读取、查看本地文件时调用。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"文件不存在: {filename}"
    except Exception as e:
        return f"读取失败: {e}"


@mcp.tool
def get_current_time() -> str:
    """获取当前日期与时间。当用户询问今天是几号、现在几点时调用。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    mcp.run()
