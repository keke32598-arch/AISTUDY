import os
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.llms import OpenAI, Ollama
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 配置
API_KEY = "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"  # OpenAI API Key
USE_OPENAI = True  # 是否使用OpenAI，False则使用本地Ollama

# 示例文档
sample_documents = [
    "RAG是检索增强生成的缩写，是一种将外部知识引入大语言模型的技术。",
    "RAG的核心思想是：检索相关文档，将其作为上下文提供给大语言模型，然后让模型基于这些文档生成回答。",
    "RAG的工作流程包括：用户提问、文本向量化、相似度搜索、上下文构建、AI生成回答。",
    "向量数据库是RAG系统的重要组成部分，用于存储和检索文本的向量表示。",
    "常见的向量数据库包括Chroma、Milvus、Pinecone等。",
    "Embedding是将文本转换为向量的过程，常用的Embedding模型包括OpenAI的text-embedding-3-small和Hugging Face的Sentence-BERT。",
    "文档分块是RAG系统中的重要步骤，合理的分块策略可以提高检索效果。",
    "检索策略包括相似度搜索、混合检索、重排序等，不同的策略适用于不同的场景。"
]

def setup_embeddings():
    """设置Embedding模型"""
    if USE_OPENAI:
        # 使用OpenAI Embedding
        return OpenAIEmbeddings(api_key=API_KEY)
    else:
        # 使用本地Hugging Face模型
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def setup_llm():
    """设置语言模型"""
    if USE_OPENAI:
        # 使用OpenAI GPT
        return OpenAI(api_key=API_KEY, model="gpt-3.5-turbo-instruct")
    else:
        # 使用本地Ollama
        return Ollama(model="qwen2.5:7b")

def create_vector_store(documents, embeddings):
    """创建向量存储"""
    # 将文档分块
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    split_docs = text_splitter.create_documents(documents)
    
    # 创建向量存储
    vector_store = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings
    )
    
    return vector_store

def setup_rag_chain(vector_store, llm):
    """设置RAG链"""
    # 创建检索器
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # 创建RAG链
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )
    
    return rag_chain

def main():
    """主函数"""
    print("=== 基础RAG实现 Demo ===")
    
    # 设置Embedding模型
    print("正在设置Embedding模型...")
    embeddings = setup_embeddings()
    
    # 设置语言模型
    print("正在设置语言模型...")
    llm = setup_llm()
    
    # 创建向量存储
    print("正在创建向量存储...")
    vector_store = create_vector_store(sample_documents, embeddings)
    
    # 设置RAG链
    print("正在设置RAG链...")
    rag_chain = setup_rag_chain(vector_store, llm)
    
    # 测试问答
    print("\n=== 测试问答 ===")
    test_questions = [
        "什么是RAG？",
        "RAG的工作流程是什么？",
        "常见的向量数据库有哪些？",
        "什么是Embedding？"
    ]
    
    for question in test_questions:
        print(f"\n问题: {question}")
        result = rag_chain.invoke(question)
        print(f"回答: {result['result']}")
        
        # 显示来源文档
        print("\n来源文档:")
        for i, doc in enumerate(result['source_documents']):
            print(f"{i+1}. {doc.page_content}")

if __name__ == "__main__":
    main()