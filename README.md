# 智能调研助手（AI Research Agent）

基于 LangChain `create_agent`（底层 LangGraph 引擎）构建的多工具 AI 调研助手：
网页搜索 + 多轮记忆 + 自研 MCP Server 工具 + 循环控制 + 报错兜底，命令行交互。

## 功能特性

- **网页搜索**：自动调用 Tavily 实时搜索，回答不受模型知识截止日期限制
- **多轮记忆**：基于 LangGraph Checkpointer，同一会话记住上下文与搜索结果（thread_id 会话隔离）
- **自研 MCP Server**：文件读写 / 时间查询工具，通过 MCP 标准协议接入工具节点
- **报错兜底**：异常捕获，崩溃不死循环
- **成本控制**：提示词约束搜索次数，避免无谓 token 消耗

## 技术栈

Python 3.13 · LangChain · LangGraph · Tavily · DeepSeek · FastMCP

## 快速开始

```bash
# 1. 安装依赖
pip install langchain langchain-tavily langgraph langchain-mcp-adapters fastmcp python-dotenv

# 2. 配置 .env（项目根目录）
TAVILY_API_KEY=你的key

# 3. 启动 MCP Server（独立进程，被 Agent 通过 stdio 调用）
python mcp_server.py

# 4. 运行 Agent
python 智能助手.py
```

## 使用示例

```
请输入要求：2026年10月最新的AI行业大新闻有哪些？
# → Agent 自动搜索 → 基于实时结果中文回答

请输入要求：把刚才的回答保存到 report.md
# → Agent 调用 MCP 文件工具写入文件

请输入要求：今天几号？
# → Agent 调用 MCP 时间工具精确回答（不靠模型瞎猜）
```

## 设计要点

- **为什么用 create_agent**：底层即 LangGraph 图引擎，封装了 state 与循环，
  快速构建工具调用 Agent；需要自定义流程时可下沉到手写 LangGraph
- **记忆方案**：checkpointer 保存完整状态（含工具调用中间消息），
  thread_id 隔离会话；对比手动拼接历史：不漏中间消息、并发安全、可平滑升级 SqliteSaver/Postgres
- **工具分层**：可复用能力（搜索、文件）走 MCP 标准协议，项目内私有逻辑用 @tool，
  两者混用是 Agent 工程的标准做法
- **成本与稳定**：system_prompt 约束搜索次数 + 异常捕获兜底，防止死循环与崩溃

## 项目结构

```
智能助手/
├── 智能助手.py      # 主程序：工具 / 模型 / Agent / 交互循环
├── mcp_server.py    # 自研 MCP Server：文件读写 + 时间工具
├── README.md
└── .gitignore
```
