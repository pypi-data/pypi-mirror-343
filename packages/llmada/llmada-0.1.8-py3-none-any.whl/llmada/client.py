"""
client.py 用于管理client
"""
import requests

class OpenAIClient:
    """
    使用 openai 官方包对接 OpenAI API，支持简单对话和流式对话
    """
    def __init__(self, api_key: str, api_base: str = "https://api.bianxie.ai/v1/chat/completions"):
        """
        初始化 OpenAI 客户端
        """
        self.api_key = api_key
        self.api_base = api_base
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

    def request(self, params: dict) -> dict:
        """
        简单对话：直接调用 OpenAI API 并返回完整响应
        """

        try:
            response = requests.post(self.api_base, headers=self.headers, json=params)
            return response.json()
        except Exception as e:
            raise Exception(f"API request failed: {e}")

