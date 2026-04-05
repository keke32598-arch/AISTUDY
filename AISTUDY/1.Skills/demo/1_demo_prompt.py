#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
提示词工程Demo
演示如何使用不同类型的提示词与AI模型交互
"""

import dashscope

# 配置API Key（用户需要自行填写）
API_KEY = "sk-05cdc8d4558b4c319e4c1244509dd4a9"
MODEL = "qwen-turbo"

# 初始化DashScope
dashscope.api_key = API_KEY

def chat_with_ai(messages, model=MODEL):
    """
    与AI模型进行聊天
    
    Args:
        messages: 消息列表，每个消息包含role和content
        model: 使用的模型名称
        
    Returns:
        AI的回复内容
    """
    try:
        # 转换消息格式为通义千问格式
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"系统: {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"用户: {msg['content']}\n"
            elif msg["role"] == "assistant":
                prompt += f"助手: {msg['content']}\n"
        
        response = dashscope.Generation.call(
            model=model,
            prompt=prompt,
            top_p=0.8
        )
        return response.output.text
    except Exception as e:
        return f"错误: {str(e)}"

def demo_basic_prompt():
    """
    演示基本提示词
    """
    print("=== 基本提示词演示 ===")
    messages = [
        {"role": "user", "content": "你好，你是谁？"}
    ]
    response = chat_with_ai(messages)
    print(f"AI回复: {response}")
    print()

def demo_specific_prompt():
    """
    演示具体明确的提示词
    """
    print("=== 具体明确的提示词演示 ===")
    messages = [
        {"role": "user", "content": "写一篇200字左右的关于人工智能在教育领域应用的短文，重点介绍AI如何帮助教师提高教学效率，语言风格专业但易懂。"}
    ]
    response = chat_with_ai(messages)
    print(f"AI回复: {response}")
    print()

def demo_role_prompt():
    """
    演示设定角色的提示词
    """
    print("=== 设定角色的提示词演示 ===")
    messages = [
        {"role": "system", "content": "你是一位专业的Python编程教师，擅长用简单易懂的语言解释复杂概念。"},
        {"role": "user", "content": "请解释什么是Python中的生成器（generator）？"}
    ]
    response = chat_with_ai(messages)
    print(f"AI回复: {response}")
    print()

def demo_example_prompt():
    """
    演示提供示例的提示词
    """
    print("=== 提供示例的提示词演示 ===")
    messages = [
        {"role": "user", "content": "请将以下中文句子翻译成英文：\n\n示例：\n中文：你好\n英文：Hello\n\n中文：谢谢\n英文："}
    ]
    response = chat_with_ai(messages)
    print(f"AI回复: {response}")
    print()

def demo_step_by_step_prompt():
    """
    演示分步骤思考的提示词
    """
    print("=== 分步骤思考的提示词演示 ===")
    messages = [
        {"role": "user", "content": "请分析如何提高Python代码的性能。首先分析影响Python性能的主要因素，然后提出具体的优化策略，最后给出一个优化前后的代码示例。"}
    ]
    response = chat_with_ai(messages)
    print(f"AI回复: {response}")
    print()

if __name__ == "__main__":
    print("提示词工程Demo\n")
    print("请确保已设置正确的API_KEY\n")
    
    # 运行各个演示
    demo_basic_prompt()
    demo_specific_prompt()
    demo_role_prompt()
    demo_example_prompt()
    demo_step_by_step_prompt()
    
    print("演示完成！")