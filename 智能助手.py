import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver

#加载本地环境配置
load_dotenv(verbose=True)

#加载工具
web_search=TavilySearch(
    max_results=2,
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)

#加载大模型
model=init_chat_model(
    model="deepseek:deepseek-flash",
)

#agent初始化

agent=create_agent(
    model=model,
    tools=[web_search,],
    checkpointer=InMemorySaver(),
    system_prompt="你是调研助手，用中文回答，最多搜索2次，信息够用就停止",
)
def answer(thread_id: str="default"):
    print("调研助手启动成功，输入 退出 即可退出")
    while True:
        user_input=input("请输入要求").strip()
        if user_input in("退出","exit", "quit"):
            print("再见")
            break
        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={"configurable": {"thread_id": thread_id}},
            )
            print(result["messages"][-1].content)
        except Exception as e:    # ← 报错兜底
            print(f"出错了（{e}），请换个问法试试")
        
        
        
if __name__ == "__main__":
    answer()