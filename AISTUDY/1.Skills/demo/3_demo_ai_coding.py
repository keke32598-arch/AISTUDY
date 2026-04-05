#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI辅助编程Demo
演示如何使用AI来辅助编程任务
"""

import dashscope

# 配置API Key（用户需要自行填写）
API_KEY = "your-api-key"
MODEL = "qwen-turbo"

# 初始化DashScope
dashscope.api_key = API_KEY

def generate_code(prompt):
    """
    根据提示生成代码
    
    Args:
        prompt: 自然语言描述的需求
        
    Returns:
        生成的代码
    """
    full_prompt = f"系统: 你是一位专业的Python编程助手，能够根据自然语言描述生成高质量的Python代码。生成的代码应该结构清晰，包含必要的注释，并处理可能的异常情况。\n用户: {prompt}\n"
    
    try:
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=full_prompt,
            top_p=0.8
        )
        return response.output.text
    except Exception as e:
        return f"错误: {str(e)}"

def explain_code(code):
    """
    解释代码
    
    Args:
        code: 要解释的代码
        
    Returns:
        代码的解释
    """
    full_prompt = f"系统: 你是一位专业的Python编程教师，擅长用简单易懂的语言解释复杂的代码。请详细解释代码的功能、逻辑和关键部分。\n用户: 请解释以下Python代码：\n{code}\n"
    
    try:
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=full_prompt,
            top_p=0.8
        )
        return response.output.text
    except Exception as e:
        return f"错误: {str(e)}"

def refactor_code(code, instructions):
    """
    重构代码
    
    Args:
        code: 要重构的代码
        instructions: 重构指令
        
    Returns:
        重构后的代码
    """
    full_prompt = f"系统: 你是一位专业的Python代码重构专家，能够根据指令优化代码结构，提高代码质量。\n用户: 请根据以下指令重构代码：\n{instructions}\n\n代码：\n{code}\n"
    
    try:
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=full_prompt,
            top_p=0.8
        )
        return response.output.text
    except Exception as e:
        return f"错误: {str(e)}"

def generate_tests(code):
    """
    为代码生成测试用例
    
    Args:
        code: 要测试的代码
        
    Returns:
        测试用例
    """
    full_prompt = f"系统: 你是一位专业的Python测试工程师，能够为代码生成全面的测试用例。生成的测试应该覆盖正常情况和边界情况。\n用户: 请为以下Python代码生成测试用例：\n{code}\n"
    
    try:
        response = dashscope.Generation.call(
            model=MODEL,
            prompt=full_prompt,
            top_p=0.8
        )
        return response.output.text
    except Exception as e:
        return f"错误: {str(e)}"

def demo_code_generation():
    """
    演示代码生成
    """
    print("=== 代码生成演示 ===")
    prompt = "写一个函数，计算列表中所有元素的平均值，处理空列表的情况"
    print(f"提示: {prompt}")
    code = generate_code(prompt)
    print(f"生成的代码:\n{code}")
    print()

def demo_code_explanation():
    """
    演示代码解释
    """
    print("=== 代码解释演示 ===")
    code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
"""
    print(f"要解释的代码:\n{code}")
    explanation = explain_code(code)
    print(f"代码解释:\n{explanation}")
    print()

def demo_code_refactoring():
    """
    演示代码重构
    """
    print("=== 代码重构演示 ===")
    code = """
def calculate_price(price, discount, tax):
    if discount > 0:
        discounted_price = price - (price * discount / 100)
    else:
        discounted_price = price
    final_price = discounted_price + (discounted_price * tax / 100)
    return final_price
"""
    instructions = "重构这个函数，使其更简洁，使用默认参数，并添加类型提示"
    print(f"要重构的代码:\n{code}")
    print(f"重构指令: {instructions}")
    refactored_code = refactor_code(code, instructions)
    print(f"重构后的代码:\n{refactored_code}")
    print()

def demo_test_generation():
    """
    演示测试生成
    """
    print("=== 测试生成演示 ===")
    code = """
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
"""
    print(f"要测试的代码:\n{code}")
    tests = generate_tests(code)
    print(f"生成的测试用例:\n{tests}")
    print()

if __name__ == "__main__":
    print("AI辅助编程Demo\n")
    print("请确保已设置正确的API_KEY\n")
    
    # 运行各个演示
    demo_code_generation()
    demo_code_explanation()
    demo_code_refactoring()
    demo_test_generation()
    
    print("演示完成！")