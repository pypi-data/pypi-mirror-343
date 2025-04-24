import os

from openai import OpenAI

from yyAutoAiframework.client.OpenAIBaseClient import OpenAIBaseClient
from yyAutoAiframework.client.OpenAIClient import OpenAIClient

"""
通义千问客户端实现
"""


class DashscopeClient(OpenAIBaseClient):

    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("DASHSCOPE_BASE_URL")
        )  # 使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL
        self.default_model = "qwen-max"
        self.default_parse_model = "qwen-max"
        self.default_fc_model = "qwen-plus"
        self.default_temperature = 0
        self.embedding_client = self
        self.embedding_model = "text-embedding-3-large"

    """
    判断是否支持Client_parese 功能
    """
    def is_client_can_parse(self) -> bool:
        return False

    def get_embeddings(self,texts,  model:str=None, dimensions=None):
        if model is None:
            model = self.embedding_model
        return self.embedding_client.get_embeddings(texts, model, dimensions)