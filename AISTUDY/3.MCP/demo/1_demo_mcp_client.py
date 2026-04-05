#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP 客户端 Demo
演示如何使用 MCP 客户端连接服务器并调用工具
"""

import requests
import json
import sys

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

class MCPClient:
    """
    MCP 客户端类
    """
    
    def __init__(self, server_url):
        """
        初始化 MCP 客户端
        
        Args:
            server_url: MCP 服务器地址
        """
        self.server_url = server_url
    
    def get_tools(self):
        """
        获取可用工具列表
        
        Returns:
            工具列表
        """
        try:
            response = requests.get(f"{self.server_url}/tools")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"错误: {str(e)}"
    
    def call_tool(self, tool_name, parameters):
        """
        调用工具
        
        Args:
            tool_name: 工具名称
            parameters: 工具参数
            
        Returns:
            工具执行结果
        """
        try:
            payload = {
                "tool": tool_name,
                "parameters": parameters
            }
            response = requests.post(f"{self.server_url}/call", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"错误: {str(e)}"

def demo_mcp_basic():
    """
    演示基本的 MCP 客户端操作
    """
    print("=== MCP 客户端基本操作演示 ===")
    
    # 这里使用一个示例 MCP 服务器地址
    # 实际使用时需要替换为真实的 MCP 服务器地址
    server_url = "http://localhost:8000/mcp"
    
    client = MCPClient(server_url)
    
    # 获取工具列表
    print("1. 获取工具列表:")
    tools = client.get_tools()
    print(f"工具列表: {json.dumps(tools, ensure_ascii=False, indent=2)}")
    print()
    
    # 调用文件读取工具（示例）
    print("2. 调用文件读取工具:")
    parameters = {
        "file_path": "example.txt",
        "encoding": "utf-8"
    }
    result = client.call_tool("read_file", parameters)
    print(f"执行结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()
    
    # 调用数据库查询工具（示例）
    print("3. 调用数据库查询工具:")
    parameters = {
        "query": "SELECT * FROM users LIMIT 5",
        "database": "example_db"
    }
    result = client.call_tool("query_database", parameters)
    print(f"执行结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()

def demo_mcp_error_handling():
    """
    演示 MCP 客户端错误处理
    """
    print("=== MCP 客户端错误处理演示 ===")
    
    # 使用不存在的服务器地址
    server_url = "http://localhost:9999/mcp"
    client = MCPClient(server_url)
    
    # 尝试获取工具列表
    print("1. 尝试连接不存在的服务器:")
    tools = client.get_tools()
    print(f"结果: {tools}")
    print()
    
    # 使用正确的服务器地址但调用不存在的工具
    server_url = "http://localhost:8000/mcp"
    client = MCPClient(server_url)
    
    print("2. 调用不存在的工具:")
    parameters = {"test": "value"}
    result = client.call_tool("non_existent_tool", parameters)
    print(f"结果: {result}")
    print()

def demo_mcp_file_operations():
    """
    演示文件操作工具的使用
    """
    print("=== 文件操作工具演示 ===")
    
    server_url = "http://localhost:8000/mcp"
    client = MCPClient(server_url)
    
    # 写入文件
    print("1. 写入文件:")
    write_parameters = {
        "file_path": "test.txt",
        "content": "Hello, MCP!\nThis is a test file.",
        "encoding": "utf-8"
    }
    write_result = client.call_tool("write_file", write_parameters)
    print(f"写入结果: {json.dumps(write_result, ensure_ascii=False, indent=2)}")
    print()
    
    # 读取文件
    print("2. 读取文件:")
    read_parameters = {
        "file_path": "test.txt",
        "encoding": "utf-8"
    }
    read_result = client.call_tool("read_file", read_parameters)
    print(f"读取结果: {json.dumps(read_result, ensure_ascii=False, indent=2)}")
    print()
    
    # 列出目录
    print("3. 列出目录:")
    list_parameters = {
        "directory": "."
    }
    list_result = client.call_tool("list_directory", list_parameters)
    print(f"目录列表: {json.dumps(list_result, ensure_ascii=False, indent=2)}")
    print()

if __name__ == "__main__":
    print("MCP 客户端 Demo\n")
    
    # 运行各个演示
    demo_mcp_basic()
    demo_mcp_error_handling()
    demo_mcp_file_operations()
    
    print("演示完成！")
    print("注意：实际运行需要先启动 MCP 服务器")