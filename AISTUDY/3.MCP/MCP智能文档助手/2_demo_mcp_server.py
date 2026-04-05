#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP 服务器 Demo
演示如何实现一个简单的 MCP 服务器
"""

# 导入必要的库
from fastapi import FastAPI, HTTPException  # FastAPI框架，用于创建API
from pydantic import BaseModel  # 数据验证库
import os  # 文件系统操作
import json  # JSON处理
import sys  # 系统操作

# 设置默认编码为utf-8，避免中文输出乱码
sys.stdout.reconfigure(encoding='utf-8')

# 创建FastAPI应用实例
app = FastAPI()

# 工具描述列表 - 定义了服务器提供的所有工具
# 每个工具都有名称、描述和参数定义
tools = [
    {
        "name": "read_file",  # 工具名称
        "description": "读取文件内容",  # 工具描述
        "parameters": {  # 参数定义
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "encoding": {
                    "type": "string",
                    "description": "文件编码",
                    "default": "utf-8"  # 默认值
                }
            },
            "required": ["file_path"]  # 必填参数
        }
    },
    {
        "name": "write_file",
        "description": "写入文件内容",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "content": {
                    "type": "string",
                    "description": "文件内容"
                },
                "encoding": {
                    "type": "string",
                    "description": "文件编码",
                    "default": "utf-8"
                }
            },
            "required": ["file_path", "content"]  # 两个必填参数
        }
    },
    {
        "name": "list_directory",
        "description": "列出目录内容",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "目录路径"
                }
            },
            "required": ["directory"]
        }
    }
]

# 工具调用请求模型 - 定义了客户端发送的请求格式
class ToolCallRequest(BaseModel):
    tool: str  # 工具名称
    parameters: dict  # 工具参数

# 工具执行结果模型 - 定义了服务器返回的响应格式
class ToolCallResponse(BaseModel):
    success: bool  # 是否成功
    result: str  # 执行结果
    error: str = None  # 错误信息（如果有）

# 定义获取工具列表的API端点
@app.get("/mcp/tools")
async def get_tools():
    """
    获取可用工具列表
    当客户端请求这个端点时，返回所有可用的工具描述
    """
    return tools  # 直接返回工具列表

# 定义调用工具的API端点
@app.post("/mcp/call")
async def call_tool(request: ToolCallRequest):
    """
    调用工具
    当客户端发送工具调用请求时，根据工具名称调用相应的处理函数
    """
    tool_name = request.tool  # 获取工具名称
    parameters = request.parameters  # 获取工具参数
    
    try:
        # 根据工具名称调用相应的处理函数
        if tool_name == "read_file":
            return await handle_read_file(parameters)  # 调用文件读取处理函数
        elif tool_name == "write_file":
            return await handle_write_file(parameters)  # 调用文件写入处理函数
        elif tool_name == "list_directory":
            return await handle_list_directory(parameters)  # 调用目录列表处理函数
        else:
            # 如果工具不存在，返回404错误
            raise HTTPException(status_code=404, detail=f"工具 {tool_name} 不存在")
    except Exception as e:
        # 如果发生其他错误，返回错误信息
        return ToolCallResponse(success=False, result="", error=str(e))

# 文件读取处理函数
async def handle_read_file(parameters):
    """
    处理文件读取请求
    """
    file_path = parameters.get("file_path")  # 获取文件路径参数
    encoding = parameters.get("encoding", "utf-8")  # 获取编码参数，默认utf-8
    
    # 检查是否提供了文件路径
    if not file_path:
        raise HTTPException(status_code=400, detail="缺少 file_path 参数")
    
    try:
        # 打开文件并读取内容
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        # 返回成功响应，包含文件内容
        return ToolCallResponse(success=True, result=content)
    except Exception as e:
        # 如果读取失败，返回500错误
        raise HTTPException(status_code=500, detail=str(e))

# 文件写入处理函数
async def handle_write_file(parameters):
    """
    处理文件写入请求
    """
    file_path = parameters.get("file_path")  # 获取文件路径
    content = parameters.get("content")  # 获取文件内容
    encoding = parameters.get("encoding", "utf-8")  # 获取编码
    
    # 检查是否提供了必要参数
    if not file_path or content is None:
        raise HTTPException(status_code=400, detail="缺少 file_path 或 content 参数")
    
    try:
        # 确保目录存在，如果不存在则创建
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 写入文件
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        # 返回成功响应
        return ToolCallResponse(success=True, result="文件写入成功")
    except Exception as e:
        # 如果写入失败，返回500错误
        raise HTTPException(status_code=500, detail=str(e))

# 目录列表处理函数
async def handle_list_directory(parameters):
    """
    处理目录列表请求
    """
    directory = parameters.get("directory")  # 获取目录路径
    
    # 检查是否提供了目录路径
    if not directory:
        raise HTTPException(status_code=400, detail="缺少 directory 参数")
    
    try:
        # 列出目录内容
        items = os.listdir(directory)
        # 区分文件和目录
        result = []
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result.append({"name": item, "type": "directory"})  # 目录
            else:
                result.append({"name": item, "type": "file"})  # 文件
        # 将结果转换为JSON字符串返回
        return ToolCallResponse(success=True, result=json.dumps(result, ensure_ascii=False))
    except Exception as e:
        # 如果列出失败，返回500错误
        raise HTTPException(status_code=500, detail=str(e))

# 主函数，启动服务器
if __name__ == "__main__":
    import uvicorn  # 导入uvicorn服务器
    print("启动 MCP 服务器...")
    print("服务器地址: http://localhost:8000")
    print("可用工具:")
    # 打印所有可用工具
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    print("按 Ctrl+C 停止服务器")
    # 启动服务器，监听所有网络接口的8000端口
    uvicorn.run(app, host="0.0.0.0", port=8000)