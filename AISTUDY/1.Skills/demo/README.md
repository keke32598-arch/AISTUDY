# Skills 章节 Demo 说明

## 学习顺序

1. 提示词工程 Demo (`1_demo_prompt.py`)
2. AI API 调用 Demo (`2_demo_api.py`)
3. AI 辅助编程 Demo (`3_demo_ai_coding.py`)

## Demo 说明

### Demo 1: 提示词工程
**文件**: `1_demo_prompt.py`

这个 Demo 演示如何使用不同类型的提示词与AI模型交互，包括基本提示词、具体明确的提示词、设定角色的提示词、提供示例的提示词和分步骤思考的提示词。

**需要 API Key**

### Demo 2: AI API 调用
**文件**: `2_demo_api.py`

这个 Demo 演示如何使用OpenAI API进行基本聊天、流式输出、多轮对话、错误处理和重试机制。

**需要 API Key**

### Demo 3: AI 辅助编程
**文件**: `3_demo_ai_coding.py`

这个 Demo 演示如何使用AI来辅助编程任务，包括代码生成、代码解释、代码重构和测试生成。

**需要 API Key**

## 对应理论文档

| Demo | 对应理论文档 | 核心知识点 |
|------|-------------|------------|
| 1_demo_prompt.py | 1.提示词工程.md | 提示词结构、优化技巧、模板 |
| 2_demo_api.py | 2.AI API调用.md | API调用流程、流式输出、错误处理 |
| 3_demo_ai_coding.py | 3.AI辅助编程.md | 代码生成、解释、重构、测试 |

## 核心要点

1. **提示词工程**：好的提示词可以显著提高AI模型的表现，包括具体明确、提供示例、设定角色等技巧。

2. **AI API调用**：掌握基本的API调用流程，包括认证、请求构建、响应处理和错误处理。

3. **AI辅助编程**：利用AI工具提高开发效率，包括代码生成、解释、重构和测试。

## 运行说明

1. 确保已安装必要的依赖：
   ```bash
   pip install dashscope
   ```

2. 在每个Demo文件中填写你的API Key：
   ```python
   API_KEY = "your-api-key"
   ```

3. 运行Demo：
   ```bash
   python 1_demo_prompt.py
   python 2_demo_api.py
   python 3_demo_ai_coding.py
   ```