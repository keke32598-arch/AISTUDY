from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.llms import OpenAI, Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# 配置
API_KEY = "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"  # OpenAI API Key
USE_OPENAI = True  # 是否使用OpenAI，False则使用本地Ollama

# 示例文档
documents = [
    "RAG是检索增强生成的缩写，是一种将外部知识引入大语言模型的技术。",
    "RAG的核心思想是：检索相关文档，将其作为上下文提供给大语言模型，然后让模型基于这些文档生成回答。",
    "RAG的工作流程包括：用户提问、文本向量化、相似度搜索、上下文构建、AI生成回答。",
    "向量数据库是RAG系统的重要组成部分，用于存储和检索文本的向量表示。",
    "常见的向量数据库包括Chroma、Milvus、Pinecone等。",
    "Embedding是将文本转换为向量的过程，常用的Embedding模型包括OpenAI的text-embedding-3-small和Hugging Face的Sentence-BERT。",
    "文档分块是RAG系统中的重要步骤，合理的分块策略可以提高检索效果。",
    "检索策略包括相似度搜索、混合检索、重排序等，不同的策略适用于不同的场景。",
    "混合检索结合了关键词搜索和向量搜索的优点，可以提高检索的准确性。",
    "重排序是对初始检索结果进行重新排序的过程，可以进一步提高检索质量。"
]

def setup_embeddings():
    """设置Embedding模型"""
    if USE_OPENAI:
        return OpenAIEmbeddings(api_key=API_KEY)
    else:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def setup_llm():
    """设置语言模型"""
    if USE_OPENAI:
        return OpenAI(api_key=API_KEY, model="gpt-3.5-turbo-instruct")
    else:
        return Ollama(model="qwen2.5:7b")

def create_vector_store(documents, embeddings):
    """创建向量存储"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = text_splitter.create_documents(documents)
    
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings
    )
    
    return vector_store

def setup_bm25_retriever(documents):
    """设置BM25检索器（关键词搜索）"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = text_splitter.create_documents(documents)
    
    bm25_retriever = BM25Retriever.from_documents(split_docs)
    bm25_retriever.k = 3
    
    return bm25_retriever

def setup_ensemble_retriever(vector_retriever, bm25_retriever):
    """设置集成检索器（混合检索）"""
    ensemble_retriever = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.7, 0.3]  # 向量检索权重70%，关键词检索权重30%
    )
    
    return ensemble_retriever

def test_retrieval_strategy(rag_chain, strategy_name, question):
    """测试检索策略"""
    print(f"\n=== 测试 {strategy_name} ===")
    print(f"问题: {question}")
    
    result = rag_chain.invoke(question)
    print(f"回答: {result['result']}")
    
    print("\n来源文档:")
    for i, doc in enumerate(result['source_documents']):
        print(f"{i+1}. {doc.page_content}")

def main():
    """主函数"""
    print("=== 检索策略 Demo ===")
    
    # 设置Embedding模型
    print("正在设置Embedding模型...")
    embeddings = setup_embeddings()
    
    # 设置语言模型
    print("正在设置语言模型...")
    llm = setup_llm()
    
    # 创建向量存储
    print("正在创建向量存储...")
    vector_store = create_vector_store(documents, embeddings)
    
    # 1. 测试相似度搜索（向量检索）
    print("\n=== 1. 相似度搜索（向量检索）===")
    vector_retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    vector_rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_retriever,
        return_source_documents=True
    )
    
    # 2. 测试BM25检索（关键词搜索）
    print("\n=== 2. BM25检索（关键词搜索）===")
    bm25_retriever = setup_bm25_retriever(documents)
    
    bm25_rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=bm25_retriever,
        return_source_documents=True
    )
    
    # 3. 测试混合检索（向量 + 关键词）
    print("\n=== 3. 混合检索（向量 + 关键词）===")
    ensemble_retriever = setup_ensemble_retriever(vector_retriever, bm25_retriever)
    
    ensemble_rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=ensemble_retriever,
        return_source_documents=True
    )
    
    # 测试问题
    test_questions = [
        "什么是RAG的核心思想？",
        "向量数据库有哪些？",
        "什么是混合检索？"
    ]
    
    # 对每个问题测试不同的检索策略
    for question in test_questions:
        print(f"\n\n====================================")
        print(f"测试问题: {question}")
        print("====================================")
        
        # 测试向量检索
        test_retrieval_strategy(vector_rag_chain, "向量检索", question)
        
        # 测试关键词检索
        test_retrieval_strategy(bm25_rag_chain, "关键词检索", question)
        
        # 测试混合检索
        test_retrieval_strategy(ensemble_rag_chain, "混合检索", question)

if __name__ == "__main__":
    main()