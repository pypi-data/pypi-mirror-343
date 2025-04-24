from openai import BaseModel

from yyAutoAiframework.agi_common.AGIExtraParam import AGIExtraParam
from yyAutoAiframework.agi_common.AGIResponse import *
from yyAutoAiframework.agi_common.PromptObject import PromptObject

"""
通用AI客户端接口类，用于定义不同AI平台（如OpenAI和通义千问）的统一接口
"""


class BaseAIClient:
    """
    获取AGI 返回的Message信息
    """

    def get_completion_response(self, messages, response_format: str = "text",
                                extra_param: AGIExtraParam = None) -> AGIResponse:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    获取 Stream 留的Message 信息
    """

    """
    定义基础UTIL 类
    """

    def get_parsed_response(self, messages, response_format: BaseModel,
                            extra_param: AGIExtraParam = None) -> AGIResponse:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    根据用户输入获取标准返回
    """

    def call_agi_by_stand_prompt(self, prompt_obj: PromptObject, response_format="text",
                                 extra_param: AGIExtraParam = None) -> AGIResponse:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    执行Prompt 的调用
    """

    def call_agi_single_msg(self, prompt: str, response_format: str = "text",
                            extra_param: AGIExtraParam = None) -> AGIResponse:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    执行Prompt 的调用
    """

    def call_agi_messages(self, messages: [], response_format: str = "text",
                          extra_param: AGIExtraParam = None) -> AGIResponse:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    执行Prompt 的调用
    """

    def get_append_response_message(self, response) -> dict:
        raise NotImplementedError("chat_completion 方法需要子类实现")

    """
    判断是否支持Client_parese 功能
    """

    def is_client_can_parse(self) -> bool:
        raise NotImplementedError("chat_completion 方法需要子类实现")


