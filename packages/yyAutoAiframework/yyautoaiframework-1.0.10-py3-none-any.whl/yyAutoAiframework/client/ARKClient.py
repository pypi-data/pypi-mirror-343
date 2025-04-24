import os

from volcenginesdkarkruntime import Ark

from yyAutoAiframework.client.OpenAIBaseClient import OpenAIBaseClient
from yyAutoAiframework.client.OpenAIClient import OpenAIClient

"""
OpenAI 客户端实现
"""
class ARKClient(OpenAIBaseClient):

    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 初始化 OpenAI 客户端
        self.client = Ark(
            api_key=os.getenv("ARK_API_KEY"),
            base_url=os.getenv("ARK_BASE_URL"),
            timeout = 120,
            max_retries=2
        )
        # self.default_model = "ep-20250102000704-2krqj"
        self.default_model = "ep-20250102001510-985qv"
        self.default_parse_model = "ep-20250102000929-phnpm"
        self.default_fc_model = "ep-20250102001510-985qv"
        self.default_temperature = 0
        self.embedding_client = OpenAIClient()
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