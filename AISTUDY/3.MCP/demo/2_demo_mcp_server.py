#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP 服务器 Demo
演示如何实现一个简单的 MCP 服务器
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import sys

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

# 工具描述
tools = [
    {
        "name": "read_file",
        "description": "读取文件内容",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "文件路径"
                },
                "encoding": {
                    "type": "string",
                    "description": "文件编码",
                    "default": "utf-8"
                }
            },
            "required": ["file_path"]
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
            "required": ["file_path", "content"]
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

# 工具调用请求模型
class ToolCallRequest(BaseModel):
    tool: str
    parameters: dict

# 工具执行结果模型
class ToolCallResponse(BaseModel):
    success: bool
    result: str
    error: str = None

@app.get("/mcp/tools")
async def get_tools():
    """
    获取可用工具列表
    """
    return tools

@app.post("/mcp/call")
async def call_tool(request: ToolCallRequest):
    """
    调用工具
    """
    tool_name = request.tool
    parameters = request.parameters
    
    try:
        if tool_name == "read_file":
            return await handle_read_file(parameters)
        elif tool_name == "write_file":
            return await handle_write_file(parameters)
        elif tool_name == "list_directory":
            return await handle_list_directory(parameters)
        else:
            raise HTTPException(status_code=404, detail=f"工具 {tool_name} 不存在")
    except Exception as e:
        return ToolCallResponse(success=False, result="", error=str(e))

async def handle_read_file(parameters):
    """
    处理文件读取
    """
    file_path = parameters.get("file_path")
    encoding = parameters.get("encoding", "utf-8")
    
    if not file_path:
        raise HTTPException(status_code=400, detail="缺少 file_path 参数")
    
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return ToolCallResponse(success=True, result=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_write_file(parameters):
    """
    处理文件写入
    """
    file_path = parameters.get("file_path")
    content = parameters.get("content")
    encoding = parameters.get("encoding", "utf-8")
    
    if not file_path or content is None:
        raise HTTPException(status_code=400, detail="缺少 file_path 或 content 参数")
    
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return ToolCallResponse(success=True, result="文件写入成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_list_directory(parameters):
    """
    处理目录列表
    """
    directory = parameters.get("directory")
    
    if not directory:
        raise HTTPException(status_code=400, detail="缺少 directory 参数")
    
    try:
        items = os.listdir(directory)
        # 区分文件和目录
        result = []
        for item in items:
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                result.append({"name": item, "type": "directory"})
            else:
                result.append({"name": item, "type": "file"})
        return ToolCallResponse(success=True, result=json.dumps(result, ensure_ascii=False))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("启动 MCP 服务器...")
    print("服务器地址: http://localhost:8000")
    print("可用工具:")
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    print("按 Ctrl+C 停止服务器")
    uvicorn.run(app, host="0.0.0.0", port=8000)