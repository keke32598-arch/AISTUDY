from langchain.document_loaders import TextLoader, PyPDFLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter

# 示例文档内容
SAMPLE_MARKDOWN = """# RAG 技术文档

## 什么是 RAG

RAG（Retrieval-Augmented Generation）是一种将外部知识引入大语言模型的技术。

### 核心思想
- **检索**：从知识库中检索与用户问题相关的文档片段
- **增强**：将检索到的文档片段作为上下文提供给大语言模型
- **生成**：大语言模型基于上下文生成回答

## RAG 的工作流程

1. **用户提问**：用户输入自然语言问题
2. **文本向量化**：将问题转换为向量表示
3. **相似度搜索**：在向量数据库中搜索相似文档
4. **上下文构建**：将检索到的文档与问题组合
5. **AI 生成**：大语言模型基于上下文生成回答

## 文档分块策略

合理的文档分块策略可以提高 RAG 系统的效果：

- **固定长度分块**：按固定字符数或 token 数分割
- **语义分块**：基于段落、句子等语义单位分割
- **滑动窗口分块**：使用重叠窗口确保上下文连续性
"""

def create_sample_files():
    """创建示例文件"""
    # 创建示例Markdown文件
    with open("sample_document.md", "w", encoding="utf-8") as f:
        f.write(SAMPLE_MARKDOWN)
    
    # 创建示例文本文件
    with open("sample_document.txt", "w", encoding="utf-8") as f:
        f.write(SAMPLE_MARKDOWN)
    
    print("创建示例文件成功")

def load_document(file_path):
    """加载文档"""
    print(f"\n=== 加载文档: {file_path} ===")
    
    if file_path.endswith(".md"):
        # 加载Markdown文件
        loader = UnstructuredMarkdownLoader(file_path)
    elif file_path.endswith(".txt"):
        # 加载文本文件
        loader = TextLoader(file_path, encoding="utf-8")
    elif file_path.endswith(".pdf"):
        # 加载PDF文件
        loader = PyPDFLoader(file_path)
    else:
        print(f"不支持的文件格式: {file_path}")
        return None
    
    documents = loader.load()
    print(f"加载的文档数量: {len(documents)}")
    print(f"文档内容:\n{documents[0].page_content[:500]}...")
    
    return documents

def test_text_splitters(documents):
    """测试不同的文本分块策略"""
    if not documents:
        return
    
    text = documents[0].page_content
    print("\n=== 测试文本分块策略 ===")
    print(f"原始文本长度: {len(text)} 字符")
    
    # 1. RecursiveCharacterTextSplitter (默认推荐)
    print("\n1. RecursiveCharacterTextSplitter:")
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    recursive_chunks = recursive_splitter.split_text(text)
    print(f"分块数量: {len(recursive_chunks)}")
    for i, chunk in enumerate(recursive_chunks[:3]):
        print(f"  块 {i+1}: {chunk[:100]}...")
    
    # 2. CharacterTextSplitter
    print("\n2. CharacterTextSplitter:")
    char_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=200,
        chunk_overlap=20
    )
    char_chunks = char_splitter.split_text(text)
    print(f"分块数量: {len(char_chunks)}")
    for i, chunk in enumerate(char_chunks[:3]):
        print(f"  块 {i+1}: {chunk[:100]}...")
    
    # 3. TokenTextSplitter
    print("\n3. TokenTextSplitter:")
    token_splitter = TokenTextSplitter(
        chunk_size=50,
        chunk_overlap=10
    )
    token_chunks = token_splitter.split_text(text)
    print(f"分块数量: {len(token_chunks)}")
    for i, chunk in enumerate(token_chunks[:3]):
        print(f"  块 {i+1}: {chunk[:100]}...")

def test_chunk_size_effect(documents):
    """测试不同分块大小的效果"""
    if not documents:
        return
    
    text = documents[0].page_content
    print("\n=== 测试不同分块大小 ===")
    
    chunk_sizes = [100, 200, 300, 500]
    for size in chunk_sizes:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=size * 0.1
        )
        chunks = splitter.split_text(text)
        print(f"分块大小 {size}: {len(chunks)} 块")
        if chunks:
            print(f"  第一块长度: {len(chunks[0])} 字符")

def main():
    """主函数"""
    print("=== 文档处理 Demo ===")
    
    # 创建示例文件
    create_sample_files()
    
    # 加载Markdown文档
    md_documents = load_document("sample_document.md")
    
    # 加载文本文档
    txt_documents = load_document("sample_document.txt")
    
    # 测试文本分块策略
    if md_documents:
        test_text_splitters(md_documents)
        test_chunk_size_effect(md_documents)

if __name__ == "__main__":
    main()