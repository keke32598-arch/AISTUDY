#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI API调用Demo
演示如何使用通义千问API进行聊天
"""

import dashscope
import time

# 配置API Key（用户需要自行填写）
API_KEY = "sk-05cdc8d4558b4c319e4c1244509dd4a9"
MODEL = "qwen-turbo"

# 初始化DashScope
dashscope.api_key = API_KEY

def basic_chat():
    """
    基本聊天功能演示
    """
    print("=== 基本聊天功能演示 ===")
    
    messages = [
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "你好，如何学习Python？"}
    ]
    
    try:
        # 转换消息格式为通义千问格式
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"系统: {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"用户: {msg['content']}\n"
        
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=prompt,
            top_p=0.8
        )
        
        print(f"AI回复: {response.output.text}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print()

def streaming_chat():
    """
    流式输出演示
    """
    print("=== 流式输出演示 ===")
    
    messages = [
        {"role": "user", "content": "写一段关于人工智能的短文，介绍AI的基本概念和应用领域。"}
    ]
    
    try:
        # 转换消息格式为通义千问格式
        prompt = ""
        for msg in messages:
            if msg["role"] == "user":
                prompt += f"用户: {msg['content']}\n"
        
        def callback(response):
            if response.output and response.output.text:
                print(response.output.text, end="")
        
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=prompt,
            top_p=0.8,
            stream=True,
            callback=callback
        )
        print()
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print()

def multi_turn_chat():
    """
    多轮对话演示
    """
    print("=== 多轮对话演示 ===")
    
    # 模拟多轮对话
    user_inputs = [
        "什么是Python中的列表推导式？",
        "请给一个例子",
        "如何在列表推导式中使用条件判断？"
    ]
    
    conversation_history = "系统: 你是一个专业的Python编程助手。\n"
    
    for input_text in user_inputs:
        print(f"用户: {input_text}")
        conversation_history += f"用户: {input_text}\n"
        
        try:
            response = dashscope.Generation.call(
                model=MODEL,
                prompt=conversation_history,
                top_p=0.8
            )
            
            assistant_response = response.output.text
            print(f"AI: {assistant_response}")
            conversation_history += f"助手: {assistant_response}\n"
        except Exception as e:
            print(f"错误: {str(e)}")
        
        print()

def error_handling_demo():
    """
    错误处理演示
    """
    print("=== 错误处理演示 ===")
    
    # 保存原始API Key
    original_api_key = dashscope.api_key
    
    # 使用无效的API Key模拟错误
    dashscope.api_key = "invalid-key"
    
    prompt = "用户: 你好\n"
    
    try:
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=prompt
        )
        print(f"AI回复: {response.output.text}")
    except Exception as e:
        print(f"认证错误: API Key无效 - {str(e)}")
    finally:
        # 恢复原始API Key
        dashscope.api_key = original_api_key
    
    print()

def retry_demo():
    """
    重试机制演示
    """
    print("=== 重试机制演示 ===")
    
    def call_with_retry(prompt, max_retries=3):
        for i in range(max_retries):
            try:
                response = dashscope.Generation.call(
                    model=MODEL,
                    prompt=f"用户: {prompt}\n"
                )
                return response
            except Exception as e:
                # 简单处理，假设所有错误都可以重试
                print(f"错误，{2 ** i}秒后重试...")
                time.sleep(2 ** i)  # 指数退避
        raise Exception("达到最大重试次数")
    
    try:
        response = call_with_retry("你好，今天天气怎么样？")
        print(f"AI回复: {response.output.text}")
    except Exception as e:
        print(f"错误: {str(e)}")
    
    print()

if __name__ == "__main__":
    print("AI API调用Demo\n")
    print("请确保已设置正确的API_KEY\n")
    
    # 运行各个演示
    basic_chat()
    streaming_chat()
    multi_turn_chat()
    error_handling_demo()
    retry_demo()
    
    print("演示完成！")