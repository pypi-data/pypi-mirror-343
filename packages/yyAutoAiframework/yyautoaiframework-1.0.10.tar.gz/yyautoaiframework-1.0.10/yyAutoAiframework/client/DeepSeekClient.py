import os

from openai import OpenAI
from yyAutoAiframework.agi_common.AGIResponse import *
from yyAutoAiframework.client.OpenAIBaseClient import OpenAIBaseClient
from yyAutoAiframework.client.OpenAIClient import OpenAIClient


class DeepSeekClient(OpenAIBaseClient):
    """
    OpenAI 客户端实现
    """
    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )  # 使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL
        # self.default_model = "deepseek-r1:70b"
        # self.default_parse_model = "deepseek-r1:70b"
        # self.default_fc_model = "deepseek-r1:70b"
        self.default_model = "deepseek-chat"
        self.default_parse_model = "deepseek-chat"
        self.default_fc_model = "deepseek-chat"
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


    @staticmethod
    def _convert_agi_response(response) -> AGIResponse:
        response_message = response.choices[0].message
        agi_response = AGIResponse().set_content(response_message.content.split("</think>")[-1]).set_role(response_message.role)
        if response_message.tool_calls is not None:
            tool_calls = []
            for tool_call in response_message.tool_calls:
                agi_tool_call = AGIToolCall(tool_call.id, tool_call.type)
                agi_tool_call.set_function(AGIToolFunction(tool_call.function.name, tool_call.function.arguments))
                tool_calls.append(agi_tool_call)
            # 添加Function Call
            agi_response.set_tool_calls(tool_calls)
        return agi_response