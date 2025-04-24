import os

import requests
from qianfan import Qianfan

from yyAutoAiframework.client.BaseAIClient import *
from yyAutoAiframework.client.OpenAIClient import OpenAIClient


class QianFanClient(OpenAIClient):
    """
    OpenAI 客户端实现
    """
    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 初始化 OpenAI 客户端
        self.client = Qianfan(
            access_key=os.getenv("QIANFAN_ACCESS_KEY"),
            secret_key=os.getenv("QIANFAN_SECRET_KEY")
        )
        self.default_model = "ernie-speed-128k"
        # self.default_parse_model = "ERNIE-4.0-8K"
        # self.default_fc_model = "ERNIE-4.0-8K"
        self.default_parse_model = "ernie-lite-8k"
        self.default_fc_model = "ernie-lite-8k"
        self.default_temperature = 0.01
        self.embedding_client = self
        self.embedding_model = "text-embedding-3-large"

    """
    获取 Stream 留的Message 信息
    """

    def _convert_stream_message(self,response):
        def update_tool_call(tool_call):
            """更新或初始化工具调用对象"""
            nonlocal tool_calls, current_tool_call_index, function_name, args, function_id, function_type
            if current_tool_call_index == -1:
                # 重置函数信息及工具调用索引
                function_name, args, function_id, function_type = "", "", "", ""
                current_tool_call_index = 0
                tool_calls.append(None)
            # 更新函数信息
            if not function_name:
                function_name = tool_call.function.name
            if not function_id:
                function_id = tool_call.id
            if not function_type:
                function_type = tool_call.type
            # 拼装参数
            return (args if args is not None else "") + \
                (tool_call.function.arguments if tool_call.function.arguments is not None else "")

        def initialize_tool_call_if_needed():
            """在需要时初始化工具调用对象"""
            if (
                    tool_calls[current_tool_call_index] is None
                    and function_id
                    and function_type
                    and function_name
            ):
                agi_tool_call = AGIToolCall(function_id, function_type)
                agi_tool_call.set_function(AGIToolFunction(function_name, args))
                tool_calls[current_tool_call_index] = agi_tool_call

            elif tool_calls[current_tool_call_index]:
                tool_calls[current_tool_call_index].get_function().set_arguments(args)

        def process_stream_response(delta_content):
            """处理流响应内容"""
            nonlocal concatenated_text
            concatenated_text += delta_content
            stream_response_list.append(StreamResponse(delta_content))

        concatenated_text, role = "", ""
        tool_calls = None
        function_name, args, function_id, function_type = "", "", "", ""
        current_tool_call_index = -1
        stream_response_list = []
        for msg in response:
            delta = msg.choices[0].delta
            if delta.tool_calls:
                # 初始化工具调用列表
                if tool_calls is None:
                    tool_calls = []
                args = update_tool_call(delta.tool_calls[0])
                initialize_tool_call_if_needed()
            elif delta.content:
                process_stream_response(delta.content)
            # if not role and delta.role:
            #     role = delta.role

        # 设置最终响应对象
        agi_response = AGIResponse().set_content(concatenated_text).set_role(role).set_stream_response(
            stream_response_list)
        if tool_calls:
            agi_response.set_tool_calls(tool_calls)

        return agi_response

    """
    判断是否支持Client_parese 功能
    """
    def is_client_can_parse(self) -> bool:
        return False


    def get_embeddings(self,texts,  model:str=None, dimensions=None):
        if model is None:
            model = self.embedding_model
        return self.embedding_client.get_embeddings(texts, model, dimensions)

    # def get_embeddings(self,texts,  model="text-embedding-ada-002", dimensions=None):
    #     access_token = self._get_access_token()
    #     print(access_token)
    #     url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_en?access_token=" + access_token
    #     payload = json.dumps({
    #         "input": texts
    #     })
    #     headers = {'Content-Type': 'application/json'}
    #
    #     response = requests.request(
    #         "POST", url, headers=headers, data=payload).json()
    #     data = response["data"]
    #     return [x["embedding"] for x in data]

    def _get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": os.getenv("QIANFAN_ACCESS_KEY"),
            "client_secret": os.getenv("QIANFAN_SECRET_KEY")
        }

        return str(requests.post(url, params=params).json().get("access_token"))