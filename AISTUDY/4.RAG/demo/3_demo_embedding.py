from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
import numpy as np

# 配置
API_KEY = "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"  # OpenAI API Key
USE_OPENAI = True  # 是否使用OpenAI，False则使用本地Hugging Face模型

# 测试文本
test_texts = [
    "RAG是检索增强生成的缩写",
    "向量数据库用于存储文本的向量表示",
    "Embedding是将文本转换为向量的过程",
    "文档分块可以提高RAG系统的效果",
    "相似度搜索是RAG的核心步骤"
]

def setup_openai_embeddings():
    """设置OpenAI Embedding模型"""
    return OpenAIEmbeddings(api_key=API_KEY)

def setup_huggingface_embeddings():
    """设置Hugging Face Embedding模型"""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_embeddings(embeddings_model, texts):
    """获取文本的Embedding"""
    return embeddings_model.embed_documents(texts)

def calculate_similarity(embedding1, embedding2):
    """计算两个向量的余弦相似度"""
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

def test_embedding_model(embeddings_model, model_name):
    """测试Embedding模型"""
    print(f"\n=== 测试 {model_name} Embedding模型 ===")
    
    # 获取文本的Embedding
    print("正在生成Embedding...")
    embeddings = get_embeddings(embeddings_model, test_texts)
    
    # 显示Embedding信息
    print(f"生成的Embedding数量: {len(embeddings)}")
    print(f"每个Embedding的维度: {len(embeddings[0])}")
    
    # 计算相似度矩阵
    print("\n相似度矩阵:")
    print("\t" + "\t".join([f"文本{i+1}" for i in range(len(test_texts))]))
    
    for i, text1 in enumerate(test_texts):
        row = [f"文本{i+1}"]
        for j, text2 in enumerate(test_texts):
            similarity = calculate_similarity(embeddings[i], embeddings[j])
            row.append(f"{similarity:.4f}")
        print("\t".join(row))
    
    # 测试查询相似度
    print("\n=== 测试查询相似度 ===")
    query = "什么是RAG？"
    print(f"查询文本: {query}")
    
    # 获取查询的Embedding
    query_embedding = embeddings_model.embed_query(query)
    
    # 计算与每个文本的相似度
    similarities = []
    for i, text in enumerate(test_texts):
        similarity = calculate_similarity(query_embedding, embeddings[i])
        similarities.append((text, similarity))
    
    # 按相似度排序
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    print("与查询的相似度排序:")
    for i, (text, similarity) in enumerate(similarities):
        print(f"{i+1}. 相似度: {similarity:.4f} - {text}")

def main():
    """主函数"""
    print("=== 文本向量化 Demo ===")
    
    if USE_OPENAI:
        # 测试OpenAI Embedding
        openai_embeddings = setup_openai_embeddings()
        test_embedding_model(openai_embeddings, "OpenAI")
    else:
        # 测试Hugging Face Embedding
        hf_embeddings = setup_huggingface_embeddings()
        test_embedding_model(hf_embeddings, "Hugging Face")

if __name__ == "__main__":
    main()