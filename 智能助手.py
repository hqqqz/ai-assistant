import asyncio
import os
import sys


from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient


# 加载本地环境配置
load_dotenv(verbose=True)

# 加载工具：网页搜索
web_search = TavilySearch(
    max_results=2,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
)

async def build_agent():
    client=MultiServerMCPClient({
        "assistant":{
            #自动加载当前解释器
            "command": sys.executable,
            "args":["mcp_server.py"],
            "transport":"stdio"
        }
    })

     #把MCP工具变成LangChain工具
    mcp_tools=await client.get_tools()

    # 加载大模型
    model = init_chat_model(model="deepseek:deepseek-flash")

     # Agent 初始化：工具调用 + 多轮记忆 + 搜索次数约束
    agent=create_agent(
        model=model,
        tools=[web_search,*mcp_tools,],
        checkpointer=InMemorySaver(),
        system_prompt="你是调研助手，用中文回答，最多搜索2次，信息够用就停止",
    )
    return agent

#问答
async def answer(agent,thread_id: str = "default"):
    """命令行多轮对话：同一 thread_id 保持记忆，exit 退出。"""
    print("调研助手启动成功，输入 退出 即可退出")
    while True:
        user_input = input("请输入要求").strip()
        if user_input in ("退出", "exit", "quit", "q"):
            print("再见")
            break
        try:
            result =await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"configurable": {"thread_id": thread_id}},
            )
            print(result["messages"][-1].content)
        except Exception as e:
            print(f"出错了（{e}），请换个问法试试")
#asyncio.run() 一次只跑一个协程，跑完循环即关闭
async def main():
    agent = await build_agent()
    await answer(agent)


if __name__ == "__main__":
    asyncio.run(main())
