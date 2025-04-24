import json
from typing import Type

from pydantic import BaseModel

from yyAutoAiframework.agi_common.AGIExtraParam import AGIExtraParam
from yyAutoAiframework.agi_common.AGIResponse import AGIResponse
from yyAutoAiframework.agi_common.DialogManagerFactory import DialogManagerFactory
from yyAutoAiframework.util.AGIUtil import AGIUtil


class DialogManager:
    authorized_caller = None

    def __init__(self, dm_factory: DialogManagerFactory,session_id: str, system_prompt: str = None, assistant_prompt: str = None):
        # 验证合法调用者
        if DialogManager.authorized_caller != "DialogManagerFactory":
            raise PermissionError("DialogManager can only be initialized by DialogManagerFactory!")
        self.state = {}
        self.session = []
        self.dm_factory = dm_factory
        self.session_id = session_id
        if system_prompt is not None:
            self.session.append({
                "role": "system",
                "content": system_prompt
            })
        if assistant_prompt is not None:
            self.session.append({
                "role": "assistant",
                "content": assistant_prompt
            })

    """
    将用户输入的信息调用AGI
    """

    def call_agi_user_message(self, user_input, response_format: [str, dict] = "text",
                              extra_param: AGIExtraParam = None) -> AGIResponse:
        self.session.append({"role": "user", "content": user_input})
        # 执行调用
        return self.call_agi_message(response_format, extra_param)

    """
    将Function Calling 生成的消息 调用AGI
    """

    def call_agi_tool_message(self, tool_call, tool_input: str, response_format: [str, dict] = "text",
                              extra_param: AGIExtraParam = None) -> AGIResponse:
        self.session.append({"tool_call_id": tool_call.id,
                             "name": tool_call.function.name,
                             "role": "tool",
                             "content": tool_input
                             })
        # 执行调用
        return self.call_agi_message(response_format, extra_param)

    """
    执行对话框的agi 调用
    """

    def call_agi_message(self, response_format: [str, dict] = "text", extra_param: AGIExtraParam = None) -> AGIResponse:
        response = self.dm_factory.client.call_agi_messages(self.session, response_format, extra_param)
        # 将当前用户输入和系统回复维护入chatgpt的session
        self.session.extend(self.dm_factory.client.get_append_response_message(response))
        return response

    """
    将用户输入的信息调用AGI,以生成对应信息的解析
    """

    def call_agi_user_parse(self, user_input, response_format: [Type[BaseModel], dict],
                            extra_param: AGIExtraParam = None) -> AGIResponse:
        self.session.append({"role": "user", "content": user_input})
        # 执行调用
        return self.call_agi_parse(response_format, extra_param)

    """
    执行对话框的agi 调用，用于生成信息解析
    """

    def call_agi_parse(self, response_format: [Type[BaseModel], dict],
                       extra_param: AGIExtraParam = None) -> AGIResponse:
        response = self.dm_factory.client.get_parsed_response(self.session, response_format, extra_param)
        # 将当前用户输入和系统回复维护入chatgpt的session
        self.session.extend(self.dm_factory.client.get_append_response_message(response))
        return response

    """
    拼接Tool Call 的message 
    """

    def append_agi_tool_message(self, tool_call, tool_input: str):
        self.session.append({"tool_call_id": tool_call.id,
                             "name": tool_call.function.name,
                             "role": "tool",
                             "content": tool_input
                             })

    """
    输出dialogManager 相关的Message 信息
    """

    def print_dm_messages(self):
        print(AGIUtil.format_json(self.session))

    """
    执行Tool Call 的逻辑
    """
    def exec_tool_calls(self,response:AGIResponse,tool_callback,extra_param: AGIExtraParam = None):
        last_function_name = ""
        # 如果返回的是函数调用结果，则打印出来
        while response.get_tool_calls() is not None:
            for tool_call in response.get_tool_calls():
                args = json.loads(tool_call.function.arguments)
                # 解决重复调用问题，目前只发现 Deepseek 有这个问题
                if last_function_name != tool_call.function.name:
                    # print("函数参数展开：%s %s" % (tool_call.function.name,AGIUtil.format_json(args)))
                    result = ""
                    # 使用回调函数执行逻辑
                    if callable(tool_callback):
                        try:
                            result = tool_callback(tool_call.function.name, args)
                        except Exception as e:
                            print(f"执行 Tool 回调发生异常: {str(e)}")
                            result = {"error": str(e)}

                        # print("%s=====函数返回=====：%s " % (tool_call.function.name,AGIUtil.format_json(result)))
                        self.append_agi_tool_message(tool_call, str(result))
                        last_function_name = tool_call.function.name

            # 执行调用
            # self.print_dm_messages()
            response = self.call_agi_message(extra_param=extra_param)

        # self.print_dm_messages()
        #返回Response
        return response