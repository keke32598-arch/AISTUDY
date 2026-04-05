# MCP 章节 Demo 说明

## 学习顺序

1. MCP 客户端 Demo (`1_demo_mcp_client.py`)
2. MCP 服务器 Demo (`2_demo_mcp_server.py`)

## Demo 说明

### Demo 1: MCP 客户端
**文件**: `1_demo_mcp_client.py`

这个 Demo 演示如何使用 MCP 客户端连接服务器并调用工具，包括获取工具列表、调用文件操作工具和错误处理。

**不需要 API Key**

### Demo 2: MCP 服务器
**文件**: `2_demo_mcp_server.py`

这个 Demo 演示如何实现一个简单的 MCP 服务器，提供文件读取、写入和目录列表等工具能力。

**不需要 API Key**

## 对应理论文档

| Demo | 对应理论文档 | 核心知识点 |
|------|-------------|------------|
| 1_demo_mcp_client.py | 1.MCP基础.md | MCP 客户端开发、工具调用 |
| 2_demo_mcp_server.py | 1.MCP基础.md | MCP 服务器实现、工具注册 |

## 核心要点

1. **MCP 工作原理**：MCP Server 提供工具能力，MCP Client 负责调用工具，通过标准化的接口进行通信。

2. **工具调用流程**：建立连接 → 工具发现 → 工具调用 → 工具执行 → 结果返回 → 结果处理。

3. **实际应用**：MCP 可以让 AI 应用轻松扩展各种工具能力，如文件操作、数据库查询、API 调用等。

## 运行说明

1. **启动 MCP 服务器**：
   ```bash
   python 2_demo_mcp_server.py
   ```

2. **运行 MCP 客户端**：
   ```bash
   python 1_demo_mcp_client.py
   ```

3. **服务器地址**：默认运行在 `http://localhost:8000`

4. **可用工具**：
   - `read_file`：读取文件内容
   - `write_file`：写入文件内容
   - `list_directory`：列出目录内容