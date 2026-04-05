#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP智能文档助手主程序
用于读取和分析文档文件，生成智能摘要，提供问答功能
"""

import sys
import os
from mcp_client import MCPClient
from doc_analyzer import DocAnalyzer
from config import (
    API_KEY, MODEL, MCP_SERVER_URL, MCP_TIMEOUT,
    APP_NAME, APP_VERSION, SUPPORTED_FILE_TYPES,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

class DocAssistant:
    """
    文档助手类
    整合MCP客户端和文档分析器，提供用户交互
    """
    
    def __init__(self):
        """
        初始化文档助手
        """
        # 初始化MCP客户端
        self.mcp_client = MCPClient(
            server_url=MCP_SERVER_URL,
            timeout=MCP_TIMEOUT
        )
        
        # 初始化文档分析器
        self.analyzer = DocAnalyzer(
            api_key=API_KEY,
            model=MODEL
        )
        
        # 存储当前处理的文档内容
        self.current_content = ""
        self.current_file = ""
    
    def check_mcp_server(self):
        """
        检查MCP服务器状态
        """
        print("检查MCP服务器状态...")
        if self.mcp_client.is_available():
            print("✓ MCP服务器可用")
            return True
        else:
            print("✗ MCP服务器不可用，将使用本地模式")
            return False
    
    def read_file(self, file_path):
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否读取成功
        """
        # 清理路径，移除可能的引号
        file_path = file_path.strip('"\'')
        
        # 检查文件类型
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in SUPPORTED_FILE_TYPES:
            print(f"错误: {ERROR_MESSAGES['INVALID_FILE_TYPE']}")
            print(f"支持的文件类型: {', '.join(SUPPORTED_FILE_TYPES)}")
            return False
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在: {file_path}")
            return False
        
        # 尝试通过MCP服务器读取文件
        print(f"正在读取文件: {file_path}")
        content = self.mcp_client.read_file(file_path)
        
        # 检查是否读取成功
        if isinstance(content, str) and not content.startswith("读取文件失败") and not "HTTPConnectionPool" in content and not "Connection refused" in content:
            self.current_content = content
            self.current_file = file_path
            print("✓ 文件读取成功哟！ (MCP服务器)")
            # 显示文件内容预览
            preview = self.current_content[:50] + "..." if len(self.current_content) > 50 else self.current_content
            print(f"文件内容预览: {preview}")
            return True
        else:
            # MCP服务器失败或返回错误信息，尝试本地读取
            print("MCP服务器读取失败或返回错误信息，尝试本地读取...")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.current_content = f.read()
                self.current_file = file_path
                print(f"✓ {SUCCESS_MESSAGES['FILE_READ_SUCCESS']} (本地模式)")
                print(f"文件大小: {len(self.current_content)} 字符")
                # 显示文件内容预览
                preview = self.current_content[:50] + "..." if len(self.current_content) > 50 else self.current_content
                print(f"文件内容预览: {preview}")
                return True
            except Exception as e:
                print(f"错误: {ERROR_MESSAGES['FILE_READ_ERROR']}: {str(e)}")
                return False
    

    
    def generate_summary(self, summary_type="brief"):
        """
        生成文档摘要
        
        Args:
            summary_type: 摘要类型 ("brief" 或 "detailed")
        """
        if not self.current_content:
            print("错误: 请先读取文档")
            return
        
        print(f"生成{('简要' if summary_type == 'brief' else '详细')}摘要...")
        summary = self.analyzer.generate_summary(self.current_content, summary_type)
        
        print(f"\n{('简要' if summary_type == 'brief' else '详细')}摘要:")
        print(summary)
        print()
    
    def answer_question(self, question):
        """
        回答关于文档的问题
        
        Args:
            question: 用户问题
        """
        if not self.current_content:
            print("错误: 请先读取文档")
            return
        
        print(f"回答问题: {question}")
        answer = self.analyzer.answer_question(self.current_content, question)
        
        print("\n回答:")
        print(answer)
        print()
    
    def show_menu(self):
        """
        显示菜单
        """
        print(f"\n{APP_NAME} v{APP_VERSION}")
        print("=" * 50)
        print("1. 检查MCP服务器状态")
        print("2. 读取文档文件")
        print("3. 生成简要摘要")
        print("4. 生成详细摘要")
        print("5. 文档问答")
        print("6. 退出")
        print("=" * 50)
    
    def run(self):
        """
        运行主程序
        """
        print(f"欢迎使用 {APP_NAME} v{APP_VERSION}！")
        print("本工具可以帮助你分析文档，生成智能摘要，以及基于文档内容回答问题。")
        
        # 检查MCP服务器状态
        self.check_mcp_server()
        
        while True:
            self.show_menu()
            
            try:
                choice = input("请输入选项编号: ")
                
                if choice == "1":
                    self.check_mcp_server()
                
                elif choice == "2":
                    file_path = input("请输入文档路径: ")
                    self.read_file(file_path)
                
                elif choice == "3":
                    self.generate_summary("brief")
                
                elif choice == "4":
                    self.generate_summary("detailed")
                
                elif choice == "5":
                    question = input("请输入问题: ")
                    self.answer_question(question)
                
                elif choice == "6":
                    print("再见！")
                    break
                
                else:
                    print("错误: 无效的选项")
                    
            except KeyboardInterrupt:
                print("\n再见！")
                break
            except Exception as e:
                print(f"错误: {str(e)}")
                continue

if __name__ == "__main__":
    # 运行文档助手
    assistant = DocAssistant()
    assistant.run()