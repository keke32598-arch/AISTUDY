# RAG Demo 学习指南

## 学习顺序

1. `1_demo_basic_rag.py` - 基础RAG实现
2. `2_demo_vector_db.py` - 向量数据库操作
3. `3_demo_embedding.py` - 文本向量化
4. `4_demo_document_processing.py` - 文档处理
5. `5_demo_retrieval_strategy.py` - 检索策略

## Demo 说明

### Demo 1: 基础RAG实现
**文件**: `1_demo_basic_rag.py`

这个Demo演示了RAG的基本流程：文本向量化、向量存储、相似度搜索、生成回答。

**需要 API Key / 不需要 API Key**
- 支持OpenAI API（需要API Key）
- 支持本地Ollama（不需要API Key）

### Demo 2: 向量数据库操作
**文件**: `2_demo_vector_db.py`

这个Demo演示了如何使用Chroma向量数据库进行向量的存储、检索和管理。

**需要 API Key / 不需要 API Key**
- 不需要API Key，使用本地Chroma

### Demo 3: 文本向量化
**文件**: `3_demo_embedding.py`

这个Demo演示了如何使用不同的Embedding模型将文本转换为向量。

**需要 API Key / 不需要 API Key**
- 支持OpenAI Embedding（需要API Key）
- 支持Hugging Face模型（不需要API Key）

### Demo 4: 文档处理
**文件**: `4_demo_document_processing.py`

这个Demo演示了如何解析和处理不同格式的文档，包括Markdown、PDF等。

**需要 API Key / 不需要 API Key**
- 不需要API Key

### Demo 5: 检索策略
**文件**: `5_demo_retrieval_strategy.py`

这个Demo演示了不同的检索策略，包括相似度搜索、混合检索和重排序。

**需要 API Key / 不需要 API Key**
- 支持OpenAI API（需要API Key）
- 支持本地Ollama（不需要API Key）

## 对应理论文档

| Demo | 对应理论文档 | 核心知识点 |
|------|-------------|-----------|
| 1_demo_basic_rag.py | 1.RAG原理.md | RAG工作流程、基本实现 |
| 2_demo_vector_db.py | 2.向量数据库.md | 向量存储、相似度搜索 |
| 3_demo_embedding.py | 3.Embedding.md | 文本向量化、模型选择 |
| 4_demo_document_processing.py | 4.文档解析.md | 文档解析、分块策略 |
| 5_demo_retrieval_strategy.py | 5.检索策略.md | 高级检索策略、结果优化 |

## 核心要点

1. **RAG基本流程**：用户提问 → 文本向量化 → 相似度搜索 → 上下文构建 → AI生成回答
2. **向量数据库**：使用Chroma等向量数据库存储和检索向量
3. **Embedding模型**：选择合适的Embedding模型进行文本向量化
4. **文档处理**：解析不同格式的文档，合理分块
5. **检索策略**：使用混合检索、重排序等策略提高检索效果

## 环境配置

1. 安装依赖：
   ```bash
   pip install langchain langchain-openai langchain-community chromadb sentence-transformers pypdf
   ```

2. 配置API Key（如果使用OpenAI）：
   - 在代码中设置 `API_KEY` 变量
   - 或设置环境变量 `OPENAI_API_KEY`

3. 本地模型配置（如果使用Ollama）：
   - 安装Ollama：https://ollama.com
   - 拉取模型：`ollama pull qwen2.5:7b`