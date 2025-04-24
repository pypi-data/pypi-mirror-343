import os

import httpx
import requests
from openai import OpenAI

from yyAutoAiframework.client.OpenAIBaseClient import OpenAIBaseClient


class OpenAIClient(OpenAIBaseClient):
    """
    OpenAI 客户端实现
    """
    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        proxy_url = os.getenv("PROXY_URL")
        http_client = httpx.Client(proxy=proxy_url)
        # 让 openai 使用这个 httpx 客户端
        openai_client = OpenAI(http_client= http_client)

        self.client = openai_client  # 使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL
        # self.default_model = "gpt-4o-mini"
        self.default_model = "gpt-4o"
        self.default_parse_model = "gpt-4o-mini-2024-07-18"
        self.default_fc_model = "gpt-4o-mini"
        self.default_temperature = 0
        self.embedding_client = self
        self.embedding_model = "text-embedding-3-large"

    """
    判断是否支持Client_parese 功能
    """

    def is_client_can_parse(self) -> bool:
        return True

    def get_embeddings(self,texts,  model:str=None, dimensions=None):
        if model is None:
            model = self.embedding_model
        return super().get_embeddings(texts, model, dimensions)
