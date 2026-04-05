#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置文件
用于管理API密钥和MCP服务器地址等配置信息
"""

# 通义千问API配置
API_KEY = "sk-05cdc8d4558b4c319e4c1244509dd4a9"  # 请替换为你的通义千问API密钥
MODEL = "qwen-turbo"  # 使用的模型名称

# MCP服务器配置
MCP_SERVER_URL = "http://localhost:8000/mcp"  # MCP服务器地址
MCP_TIMEOUT = 30  # MCP服务器请求超时时间（秒）

# 应用配置
APP_NAME = "MCP智能文档助手"
APP_VERSION = "1.0.0"

# 支持的文件格式
SUPPORTED_FILE_TYPES = [
    ".txt",  # 文本文件
    ".md",   # Markdown文件
    ".csv"   # CSV文件
]

# 摘要配置
SUMMARY_LENGTH = {
    "brief": 200,  # 简要摘要长度（字）
    "detailed": 500  # 详细摘要长度（字）
}

# 日志配置
LOG_LEVEL = "INFO"  # 日志级别：DEBUG, INFO, WARNING, ERROR

# 错误消息
ERROR_MESSAGES = {
    "FILE_NOT_FOUND": "文件未找到",
    "FILE_READ_ERROR": "文件读取失败",
    "API_ERROR": "API调用失败",
    "MCP_SERVER_ERROR": "MCP服务器错误",
    "INVALID_FILE_TYPE": "不支持的文件类型"
}

# 成功消息
SUCCESS_MESSAGES = {
    "FILE_READ_SUCCESS": "文件读取成功",
    "SUMMARY_GENERATED": "摘要生成成功",
    "QUESTION_ANSWERED": "问题回答成功"
}