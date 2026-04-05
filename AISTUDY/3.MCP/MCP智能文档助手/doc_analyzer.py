#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档分析模块
用于处理文档内容，提取关键信息，生成智能摘要和回答问题
"""

import dashscope
import sys
import re

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

class DocAnalyzer:
    """
    文档分析类
    用于处理文档内容，提取关键信息，生成智能摘要和回答问题
    """
    
    def __init__(self, api_key, model="qwen-turbo"):
        """
        初始化文档分析器
        
        Args:
            api_key: 通义千问API密钥
            model: 使用的模型名称
        """
        self.api_key = api_key
        self.model = model
        # 初始化DashScope
        dashscope.api_key = api_key
    
    def analyze_document(self, content):
        """
        分析文档内容
        
        Args:
            content: 文档内容
            
        Returns:
            分析结果，包含文档长度、关键词等信息
        """
        # 计算文档长度
        total_chars = len(content)
        total_words = len(content.split())
        
        # 提取关键词（简单实现）
        keywords = self._extract_keywords(content)
        
        # 分析文档结构
        structure = self._analyze_structure(content)
        
        return {
            "total_chars": total_chars,
            "total_words": total_words,
            "keywords": keywords,
            "structure": structure
        }
    
    def generate_summary(self, content, summary_type="brief"):
        """
        生成文档摘要
        
        Args:
            content: 文档内容
            summary_type: 摘要类型 ("brief" 或 "detailed")
            
        Returns:
            文档摘要
        """
        # 根据摘要类型构建提示词
        if summary_type == "brief":
            prompt = f"请对以下文档内容进行简要总结，控制在200字以内：\n\n{content}"
        else:
            prompt = f"请对以下文档内容进行详细总结，包括主要观点、关键信息和结论：\n\n{content}"
        
        # 调用AI模型生成摘要
        try:
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                top_p=0.8
            )
            return response.output.text
        except Exception as e:
            return f"生成摘要失败: {str(e)}"
    
    def answer_question(self, content, question):
        """
        基于文档内容回答问题
        
        Args:
            content: 文档内容
            question: 用户问题
            
        Returns:
            回答内容
        """
        # 构建提示词
        prompt = f"请根据以下文档内容回答问题：\n\n文档内容：\n{content}\n\n问题：{question}\n\n回答："
        
        # 调用AI模型回答问题
        try:
            response = dashscope.Generation.call(
                model=self.model,
                prompt=prompt,
                top_p=0.8
            )
            return response.output.text
        except Exception as e:
            return f"回答问题失败: {str(e)}"
    
    def _extract_keywords(self, content):
        """
        提取关键词
        
        Args:
            content: 文档内容
            
        Returns:
            关键词列表
        """
        # 简单的关键词提取实现
        # 移除标点符号
        content = re.sub(r'[\s\p{P}\p{S}]+', ' ', content)
        # 分词
        words = content.split()
        # 统计词频
        word_freq = {}
        for word in words:
            if len(word) > 1:  # 过滤单个字符
                word_freq[word] = word_freq.get(word, 0) + 1
        # 排序并返回前10个高频词
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:10]]
    
    def _analyze_structure(self, content):
        """
        分析文档结构
        
        Args:
            content: 文档内容
            
        Returns:
            文档结构信息
        """
        # 简单的文档结构分析
        lines = content.split('\n')
        paragraphs = [line.strip() for line in lines if line.strip()]
        
        # 识别标题（简单实现）
        headers = []
        for i, line in enumerate(paragraphs):
            if line.startswith('#') or line.endswith(':') or len(line) < 30:
                headers.append((i, line))
        
        return {
            "total_paragraphs": len(paragraphs),
            "headers": headers[:5]  # 返回前5个可能的标题
        }
    
    def process_file_content(self, file_path, content):
        """
        处理文件内容
        
        Args:
            file_path: 文件路径
            content: 文件内容
            
        Returns:
            处理结果
        """
        # 分析文档
        analysis = self.analyze_document(content)
        
        # 生成摘要
        brief_summary = self.generate_summary(content, "brief")
        detailed_summary = self.generate_summary(content, "detailed")
        
        return {
            "file_path": file_path,
            "analysis": analysis,
            "brief_summary": brief_summary,
            "detailed_summary": detailed_summary
        }

if __name__ == "__main__":
    # 测试文档分析器
    import os
    
    # 读取测试文件
    test_content = """
    MCP（Model Context Protocol）是一种让AI模型能够连接外部工具和数据的标准协议。
    
    ## MCP的核心组件
    - MCP Server：提供工具能力的服务器
    - MCP Client：调用工具的客户端
    
    ## MCP的工作原理
    1. AI模型通过MCP Client发送工具调用请求
    2. MCP Server执行工具操作
    3. MCP Server返回执行结果给MCP Client
    4. MCP Client将结果传递给AI模型
    
    MCP使得AI模型能够超越自身的知识范围，与外部世界进行交互。
    """
    
    # 初始化文档分析器
    # 注意：这里需要设置真实的API密钥
    api_key = "your-api-key"
    analyzer = DocAnalyzer(api_key)
    
    # 分析文档
    analysis = analyzer.analyze_document(test_content)
    print("文档分析结果:")
    print(analysis)
    
    # 生成摘要
    print("\n简要摘要:")
    brief_summary = analyzer.generate_summary(test_content, "brief")
    print(brief_summary)
    
    print("\n详细摘要:")
    detailed_summary = analyzer.generate_summary(test_content, "detailed")
    print(detailed_summary)
    
    # 回答问题
    print("\n回答问题:")
    question = "MCP的核心组件有哪些？"
    answer = analyzer.answer_question(test_content, question)
    print(f"问题: {question}")
    print(f"回答: {answer}")