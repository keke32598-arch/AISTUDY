#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP客户端模块
用于与第三方MCP服务器通信，调用文件读取等工具
"""

import requests
import json
import sys

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

class MCPClient:
    """
    MCP客户端类
    用于与第三方MCP服务器通信
    """
    
    def __init__(self, server_url="http://localhost:8000/mcp", timeout=30):
        """
        初始化MCP客户端
        
        Args:
            server_url: MCP服务器地址
            timeout: 请求超时时间（秒）
        """
        self.server_url = server_url
        self.timeout = timeout
    
    def call_tool(self, tool_name, parameters):
        """
        调用MCP工具
        
        Args:
            tool_name: 工具名称
            parameters: 工具参数
            
        Returns:
            工具执行结果，格式为：
            {
                "success": bool,  # 是否成功
                "result": str,    # 结果内容
                "error": str      # 错误信息（如果有）
            }
        """
        try:
            # 构建请求 payload
            payload = {
                "tool": tool_name,
                "parameters": parameters
            }
            
            # 发送 POST 请求到 MCP 服务器
            response = requests.post(
                f"{self.server_url}/call",
                json=payload,
                timeout=self.timeout
            )
            
            # 检查响应状态码
            response.raise_for_status()
            
            # 解析响应结果
            result = response.json()
            return result
            
        except requests.exceptions.RequestException as e:
            # 处理网络请求异常
            return {
                "success": False,
                "result": "",
                "error": f"网络请求失败: {str(e)}"
            }
        except json.JSONDecodeError as e:
            # 处理 JSON 解析异常
            return {
                "success": False,
                "result": "",
                "error": f"响应解析失败: {str(e)}"
            }
        except Exception as e:
            # 处理其他异常
            return {
                "success": False,
                "result": "",
                "error": f"未知错误: {str(e)}"
            }
    
    def read_file(self, file_path):
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容或错误信息
        """
        result = self.call_tool("read_file", {"file_path": file_path})
        if result.get("success"):
            return result.get("result", "")
        else:
            return result.get("error", "读取文件失败")
    
    def list_directory(self, directory_path):
        """
        列出目录内容
        
        Args:
            directory_path: 目录路径
            
        Returns:
            目录内容列表或错误信息
        """
        result = self.call_tool("list_directory", {"directory_path": directory_path})
        if result.get("success"):
            try:
                return json.loads(result.get("result", "[]"))
            except json.JSONDecodeError:
                return result.get("result", "")
        else:
            return result.get("error", "列出目录失败")
    
    def write_file(self, file_path, content):
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            content: 文件内容
            
        Returns:
            操作结果或错误信息
        """
        result = self.call_tool("write_file", {
            "file_path": file_path,
            "content": content
        })
        if result.get("success"):
            return "文件写入成功"
        else:
            return result.get("error", "文件写入失败")
    
    def is_available(self):
        """
        检查MCP服务器是否可用
        
        Returns:
            bool: 服务器是否可用
        """
        try:
            response = requests.get(f"{self.server_url}/tools", timeout=self.timeout)
            return response.status_code == 200
        except:
            return False

if __name__ == "__main__":
    # 测试 MCP 客户端
    client = MCPClient()
    
    # 检查服务器是否可用
    print(f"MCP服务器状态: {'可用' if client.is_available() else '不可用'}")
    
    # 测试列出目录
    print("\n测试列出目录:")
    result = client.list_directory(".")
    print(result)
    
    # 测试读取文件
    print("\n测试读取文件:")
    result = client.read_file("test.txt")
    print(result)