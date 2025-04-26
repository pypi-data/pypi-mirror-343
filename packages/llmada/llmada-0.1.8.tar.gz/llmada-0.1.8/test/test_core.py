import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from dotenv import load_dotenv
from llmada import BianXieAdapter, KimiAdapter, ArkAdapter
import os

load_dotenv()

class Test_Bianxie:
    @pytest.fixture
    def bianxie(self):
        return BianXieAdapter(api_key=os.getenv('BIANXIE_API_KEY'))

    def test_product(self,bianxie):
        bianxie.set_model('gpt-4o')
        result = bianxie.product(prompt='你好')
        print(result)
        assert type(result) == str

    def test_chat(self,bianxie):
        bianxie.set_model('gpt-4o')
        result = bianxie.chat(messages=[{'role': 'user', 'content': '你好'}])
        print(result)
        assert type(result) == str

    def test_no_api_key(self):
        bianxie = BianXieAdapter()
        bianxie.set_model('gpt-4o')
        result = bianxie.product(prompt='你好')
        print(result)
        assert type(result) == str

class Test_Kimi:

    @pytest.fixture
    def kimi(self):
        return KimiAdapter(api_key=os.getenv('MOONSHOT_API_KEY'))

    def test_product(self,kimi):
        kimi.set_model('moonshot-v1-128k')
        result = kimi.product(prompt='你好')
        print(result)
        assert type(result) == str


    def test_chat(self,kimi):
        kimi.set_model('moonshot-v1-128k')
        result = kimi.chat(messages=[{'role': 'user', 'content': '你好'}])
        print(result)
        assert type(result) == str

    def test_no_api_key(self):
        kimi = KimiAdapter()
        kimi.set_model('moonshot-v1-128k')
        result = kimi.product(prompt='你好')
        print(result)
        assert type(result) == str


class Test_Ark:

    @pytest.fixture
    def ark(self):
        return ArkAdapter(api_key=os.getenv('ARK_API_KEY'))

    def test_product(self,ark):
        ark.set_model('doubao-1-5-pro-256k-250115')
        result = ark.product(prompt='你好')
        print(result)
        assert type(result) == str


    def test_chat(self,ark):
        ark.set_model('doubao-1-5-pro-256k-250115')
        result = ark.chat(messages=[{'role': 'user', 'content': '你好'}])
        print(result)
        assert type(result) == str

    def test_no_api_key(self):
        ark = ArkAdapter()
        ark.set_model('doubao-1-5-pro-256k-250115')
        result = ark.product(prompt='你好')
        print(result)
        assert type(result) == str