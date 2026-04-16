from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 配置
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 本地Embedding模型

# 示例文档
documents = [
    {
        "id": "1",
        "content": "RAG是检索增强生成的缩写，是一种将外部知识引入大语言模型的技术。",
        "metadata": {"category": "RAG", "source": "doc1"}
    },
    {
        "id": "2",
        "content": "向量数据库是RAG系统的重要组成部分，用于存储和检索文本的向量表示。",
        "metadata": {"category": "vector_db", "source": "doc2"}
    },
    {
        "id": "3",
        "content": "常见的向量数据库包括Chroma、Milvus、Pinecone等。",
        "metadata": {"category": "vector_db", "source": "doc3"}
    },
    {
        "id": "4",
        "content": "Embedding是将文本转换为向量的过程，常用的Embedding模型包括OpenAI的text-embedding-3-small和Hugging Face的Sentence-BERT。",
        "metadata": {"category": "embedding", "source": "doc4"}
    },
    {
        "id": "5",
        "content": "文档分块是RAG系统中的重要步骤，合理的分块策略可以提高检索效果。",
        "metadata": {"category": "document", "source": "doc5"}
    }
]

def setup_embeddings():
    """设置Embedding模型"""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def create_vector_store(embeddings):
    """创建向量存储"""
    # 准备文档内容和元数据
    texts = [doc["content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    ids = [doc["id"] for doc in documents]
    
    # 创建向量存储
    vector_store = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"向量存储创建成功，包含 {vector_store._collection.count()} 个文档")
    return vector_store

def test_similarity_search(vector_store):
    """测试相似度搜索"""
    print("\n=== 测试相似度搜索 ===")
    
    # 测试查询
    query = "什么是向量数据库？"
    print(f"查询: {query}")
    
    # 相似度搜索
    results = vector_store.similarity_search(
        query=query,
        k=3
    )
    
    print("搜索结果:")
    for i, result in enumerate(results):
        print(f"{i+1}. 相似度: {result.metadata.get('score', 'N/A')}")
        print(f"   内容: {result.page_content}")
        print(f"   元数据: {result.metadata}")

def test_similarity_search_with_score(vector_store):
    """测试带分数的相似度搜索"""
    print("\n=== 测试带分数的相似度搜索 ===")
    
    # 测试查询
    query = "什么是Embedding？"
    print(f"查询: {query}")
    
    # 带分数的相似度搜索
    results = vector_store.similarity_search_with_score(
        query=query,
        k=3
    )
    
    print("搜索结果:")
    for i, (result, score) in enumerate(results):
        print(f"{i+1}. 相似度分数: {score:.4f}")
        print(f"   内容: {result.page_content}")
        print(f"   元数据: {result.metadata}")

def test_metadata_filtering(vector_store):
    """测试元数据过滤"""
    print("\n=== 测试元数据过滤 ===")
    
    # 测试查询
    query = "RAG相关内容"
    print(f"查询: {query}")
    
    # 带元数据过滤的搜索
    results = vector_store.similarity_search(
        query=query,
        k=3,
        filter={"category": "RAG"}
    )
    
    print("过滤结果 (只显示category为RAG的文档):")
    for i, result in enumerate(results):
        print(f"{i+1}. 内容: {result.page_content}")
        print(f"   元数据: {result.metadata}")

def test_add_and_delete(vector_store):
    """测试添加和删除文档"""
    print("\n=== 测试添加和删除文档 ===")
    
    # 添加新文档
    new_doc = "RAG系统的核心组件包括：文档解析器、Embedding模型、向量数据库、检索器和语言模型。"
    vector_store.add_texts(
        texts=[new_doc],
        metadatas=[{"category": "RAG", "source": "doc6"}],
        ids=["6"]
    )
    print(f"添加文档后，向量存储包含 {vector_store._collection.count()} 个文档")
    
    # 删除文档
    vector_store.delete(ids=["6"])
    print(f"删除文档后，向量存储包含 {vector_store._collection.count()} 个文档")

def main():
    """主函数"""
    print("=== 向量数据库操作 Demo ===")
    
    # 设置Embedding模型
    print("正在设置Embedding模型...")
    embeddings = setup_embeddings()
    
    # 创建向量存储
    print("正在创建向量存储...")
    vector_store = create_vector_store(embeddings)
    
    # 测试相似度搜索
    test_similarity_search(vector_store)
    
    # 测试带分数的相似度搜索
    test_similarity_search_with_score(vector_store)
    
    # 测试元数据过滤
    test_metadata_filtering(vector_store)
    
    # 测试添加和删除文档
    test_add_and_delete(vector_store)

if __name__ == "__main__":
    main()