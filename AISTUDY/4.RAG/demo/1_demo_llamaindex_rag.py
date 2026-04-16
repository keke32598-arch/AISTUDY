# LlamaIndex 高级RAG实现（支持文档上传和交互式问答）

import os
import glob
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.dashscope import DashScope
from llama_index.embeddings.dashscope import DashScopeEmbedding

# 配置
DASHSCOPE_API_KEY = "sk-38b3749850774300aea10c0f63bff3f9"  # 通义千问API Key
UPLOAD_DIR = "uploaded_docs"  # 上传文档存储目录


# 创建上传目录
def create_upload_dir():
    """创建上传文档目录"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
        print(f"创建上传目录: {UPLOAD_DIR}")
    else:
        print(f"上传目录已存在: {UPLOAD_DIR}")

# 清理旧的示例文档
def clean_old_documents():
    """清理旧的示例文档"""
    for file in glob.glob("sample_doc_*.txt"):
        os.remove(file)
    print("清理旧文档完成")

def main():
    """主函数"""
    print("基于LlamaIndex框架实现RAG数据库问答系统")
    
    # 创建上传目录
    create_upload_dir()
    
    # 清理旧文档
    clean_old_documents()
    
    # 1. 配置模型
    print("\n1. 配置模型...")
    llm = DashScope(
        model_name="qwen-max",
        api_key=DASHSCOPE_API_KEY
    )
    embed_model = DashScopeEmbedding(
        model_name="text-embedding-v4",
        api_key=DASHSCOPE_API_KEY
    )
    
    # 2. 提示用户上传文档
    print("\n2. 文档上传...")
    print("请将您要上传的文档放入以下目录:")
    print(f"{os.path.abspath(UPLOAD_DIR)}")
    input("放入文档后，按回车键继续...")
    
    # 3. 加载文档
    print("\n3. 加载文档...")
    documents = SimpleDirectoryReader(UPLOAD_DIR).load_data()
    print(f"加载了 {len(documents)} 个文档")
    
    if len(documents) == 0:
        print("未找到文档，请确保您已将文档放入上传目录")
        return
    
    # 4. 创建向量索引
    print("\n4. 创建向量索引...")
    index = VectorStoreIndex.from_documents(
        documents=documents,
        llm=llm,
        embed_model=embed_model
    )
    
    # 5. 创建查询引擎
    print("\n5. 创建查询引擎...")
    query_engine = index.as_query_engine(llm=llm)
    
    # 6. 交互式问答
    print("\n6. 交互式问答...")
    print("您可以开始提问了，输入 'exit' 退出")
    
    while True:
        question = input("\n请输入您的问题: ")
        
        if question.lower() == 'exit':
            print("退出问答系统")
            break
        
        if not question.strip():
            continue
        
        print("\n正在处理您的问题...")
        response = query_engine.query(question)
        
        print(f"\n回答: {response.response}")
        
       

if __name__ == "__main__":
    main()