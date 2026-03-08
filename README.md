# LangChain ReAct Agent 项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

## 项目简介

这是一个基于 **LangChain** 框架构建的 **ReAct (Reasoning + Acting)** 模式智能代理项目。项目集成了 RAG 检索增强生成、多工具协作、中间件拦截等功能，适用于构建需要复杂推理和多工具调用的智能对话系统。

## 核心特性

- 🤖 **ReAct Agent**: 基于 LangChain 的 ReAct 模式智能代理
- 📚 **RAG 检索增强**: 集成 ChromaDB 向量数据库，支持知识库检索
- 🔧 **多工具协作**: 支持天气查询、用户信息获取、外部数据检索等多种工具
- 🔌 **中间件机制**: 支持工具监控、日志记录、提示词动态切换
- 🌊 **流式输出**: 支持流式响应，提升用户体验

## 技术栈

### 核心框架
- **LangChain**: LLM 应用开发框架
- **LangGraph**: 工作流编排（Agent 状态管理）

### 模型服务
- **通义千问 (Qwen)**: 阿里云大语言模型
- **DashScope Embeddings**: 文本向量化模型

### 向量数据库
- **ChromaDB**: 本地向量数据库

### 配置管理
- **YAML**: 配置文件格式

## 项目结构

```
Agent项目/
├── agent/                  # Agent 核心模块
│   ├── react_agent.py     # ReAct Agent 实现
│   └── tools/             # 工具集
│       ├── agent_tools.py # Agent 工具定义
│       └── middleware.py  # 中间件实现
├── model/                  # 模型工厂
│   └── factory.py         # 模型实例化工厂
├── rag/                    # RAG 检索模块
│   ├── rag_service.py     # RAG 服务
│   └── vector_store.py    # 向量存储服务
├── prompts/                # 提示词模板
├── config/                 # 配置文件
│   ├── rag.yml            # RAG 配置
│   ├── chroma.yml         # 向量库配置
│   ├── prompts.yml        # 提示词配置
│   └── agent.yml          # Agent 配置
├── data/                   # 数据文件
│   └── external/          # 外部数据
├── chroma_db/              # ChromaDB 向量数据库
├── logs/                   # 日志文件
└── utils/                  # 工具函数
    ├── config_handler.py  # 配置加载器
    ├── prompt_loader.py   # 提示词加载器
    ├── logger_handler.py  # 日志处理器
    └── path_tool.py       # 路径工具
```

## 工具集说明

| 工具名称 | 功能描述 |
|---------|---------|
| `rag_summarize` | 从向量库中检索参考资料并生成摘要 |
| `get_weather` | 获取指定城市的天气信息 |
| `get_user_id` | 获取当前用户 ID |
| `get_user_city` | 获取用户所在城市名称 |
| `get_current_month` | 获取当前月份 |
| `fetch_external_data` | 从外部系统获取用户使用记录 |
| `fill_context_for_report` | 触发报告生成场景的上下文注入 |

## 中间件说明

| 中间件名称 | 功能描述 |
|-----------|---------|
| `monitor_tool` | 监控工具调用情况 |
| `log_before_model` | 记录模型调用前的日志 |
| `report_prompt_switch` | 报告场景提示词动态切换 |

## 快速开始

### 环境要求
- Python 3.11+
- 通义千问 API Key

### 安装依赖

```bash
pip install langchain langchain-community chromadb dashscope pyyaml
```

### 配置 API Key

在环境变量中设置通义千问 API Key：

```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

## 架构设计

```
用户查询
    ↓
ReAct Agent (推理+行动)
    ↓
工具选择与执行
    ├── RAG 检索
    ├── 天气查询
    ├── 用户信息
    └── 外部数据
    ↓
中间件处理
    ├── 监控工具调用
    ├── 记录日志
    └── 动态切换提示词
    ↓
模型生成回复
    ↓
流式输出返回用户
```

## 使用场景

1. **智能客服**: 多工具协作回答用户问题
2. **报告生成**: 自动收集数据生成使用报告
3. **知识问答**: RAG 检索知识库回答专业问题
4. **数据分析**: 从外部系统获取数据进行智能分析

## 开发指南

### 添加新工具

在 `agent/tools/agent_tools.py` 中添加：

```python
from langchain_core.tools import tool

@tool(description="工具功能描述")
def your_new_tool(param: str) -> str:
    # 实现工具逻辑
    return "结果"
```

然后在 `react_agent.py` 中注册工具。

### 添加新中间件

在 `agent/tools/middleware.py` 中实现中间件逻辑。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，欢迎提交 Issue。

---

**最后更新**: 2026年2月28日
