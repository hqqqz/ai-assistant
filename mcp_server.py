"""
文件读写+时间查询工具
"""
import time

from fastmcp import FastMCP

mcp=FastMCP()

@mcp.tool
def save_to_file(filename:str,content:str)->str:
    """保存文本内容到指定文件，当用户要求把结果/报告保存,写入文件时调用"""
    try:
        with open(filename,'w',encoding="utf-8") as f:
            f.write(content)
        return f"已保存到{filename}"
    except Exception as e:
        return f"保存失败{e}"


@mcp.tool
def read_file(filename:str)->str:
    """
    读取本地文件内容，让用户要求读取，查看本地文件时调用
    """
    try:
        with open(filename,'r',encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"文件不存在{filename}"
    except Exception as e:
        return f"保存失败{filename}"
@mcp.tool
def get_current_time():
    """
    获取当前时间，当用户询问今天是几号，现在是几点时候调用，用户的要求中含有时间问题也调用
    """
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

if __name__ == "__main__":
    mcp.run()