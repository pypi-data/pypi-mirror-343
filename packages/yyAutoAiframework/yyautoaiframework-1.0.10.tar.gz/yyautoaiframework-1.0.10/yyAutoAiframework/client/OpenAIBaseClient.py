from typing import Type

from dotenv import load_dotenv, find_dotenv

from yyAutoAiframework.client.BaseAIClient import *
from yyAutoAiframework.util.AGIUtil import AGIUtil


class OpenAIBaseClient(BaseAIClient):
    """
    OpenAI 客户端实现
    """
    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        _ = load_dotenv(find_dotenv())
        self.client = None

    """
    定义基础UTIL 类
    """

    """
    获取AGI 返回的Message信息
    """

    def get_completion_response(self, messages, response_format: [str, dict,Type[BaseModel]] = "text",
                                extra_param: AGIExtraParam = None) -> AGIResponse:
        response_format = response_format or "text"
        # 设置默认值
        if extra_param is None:
            extra_param = AGIExtraParam(self)

        if isinstance(response_format, str):
            response_format = {"type": response_format}
        #如果是有tools 信息，则代表要执行funtion_calling ，则使用Fc_model
        chat_model = extra_param.model
        if extra_param.tools:
            chat_model = extra_param.fc_model

        if response_format == "text" or response_format == "json_object" or isinstance(response_format, dict):
            response = self.client.chat.completions.create(
                model=chat_model,
                messages=messages,
                temperature=extra_param.temperature,  # 模型输出的随机性，0 表示随机性最小
                # 返回消息的格式，text 或 json_object
                response_format=response_format,
                tools=extra_param.tools,
                stream=extra_param.stream,
            )
            if extra_param.stream:
                return self._convert_stream_message(response)
            else:
                return self._convert_agi_response(response)

        elif response_format is not None and isinstance(response_format, type) and self.is_client_can_parse():
            response = self.client.beta.chat.completions.parse(
                model=chat_model,
                messages=messages,
                temperature=extra_param.temperature,
                response_format=response_format,
            )
            response_message = response.choices[0].message
            return (AGIResponse().set_content(
                (AGIUtil.format_json(response_message.parsed) if response_message.parsed is not None else None))
                    .set_tool_calls(response_message.tool_calls)
                    .set_role(response_message.role))
        else:
            raise Exception("response_format 不支持")


    """
    获取 completion 的Message 信息
    """
    @staticmethod
    def _convert_agi_response(response) -> AGIResponse:
        reponse_message = response.choices[0].message
        agi_response = AGIResponse().set_content(reponse_message.content).set_role(reponse_message.role)
        if reponse_message.tool_calls is not None:
            tool_calls = []
            for tool_call in reponse_message.tool_calls:
                agi_tool_call = AGIToolCall(tool_call.id, tool_call.type)
                agi_tool_call.set_function(AGIToolFunction(tool_call.function.name, tool_call.function.arguments))
                tool_calls.append(agi_tool_call)
            # 添加Function Call
            agi_response.set_tool_calls(tool_calls)
        return agi_response

    """
    获取Stream 流对应的Message
    """
    def _convert_stream_message(self,response) -> AGIResponse:
        def update_tool_call(tool_call):
            """更新或初始化工具调用对象"""
            nonlocal tool_calls, current_tool_call_index, function_name, args, function_id, function_type
            if tool_call.index != current_tool_call_index:
                # 重置函数信息及工具调用索引
                function_name, args, function_id, function_type = "", "", "", ""
                current_tool_call_index = tool_call.index
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
            if not role and delta.role:
                role = delta.role

        # 设置最终响应对象
        agi_response = AGIResponse().set_content(concatenated_text).set_role(role).set_stream_response(
            stream_response_list)
        if tool_calls:
            agi_response.set_tool_calls(tool_calls)

        return agi_response

    """
    根据用户输入获取标准返回
    """

    def call_agi_by_stand_prompt(self, prompt_obj: PromptObject, response_format="text",
                                 extra_param: AGIExtraParam = None) -> AGIResponse:
        response_format = response_format or "text"
        prompt_template = f"""
        # 目标
        {prompt_obj.instruction}
        # 输出格式
        {prompt_obj.output_format}
        # 对话上下文
        {prompt_obj.context}
        """

        if prompt_obj.example is not None and prompt_obj.example != "":
            prompt_template = prompt_template + f"""
        # 举例
        {prompt_obj.example}
            """
        # print(prompt_template)
        # 执行调用
        return self.call_agi_single_msg(prompt_template, response_format, extra_param)

    """
    执行Prompt 的调用
    """

    def call_agi_single_msg(self, prompt: str, response_format: [str, dict,Type[BaseModel]] = "text",
                            extra_param: AGIExtraParam = None) -> AGIResponse:
        messages = [{"role": "user", "content": prompt}]  # 将 prompt 作为用户输入
        response = self.call_agi_messages(messages, response_format, extra_param)
        return response

    """
    执行Prompt 的调用
    """

    def call_agi_messages(self, messages: [], response_format: [str, dict,Type[BaseModel]] = "text",
                          extra_param: AGIExtraParam = None) -> AGIResponse:

        return self.get_completion_response(messages, response_format=response_format, extra_param=extra_param)

    """
    拼接Response 的信息，加入对话的上下文中
    """

    def get_append_response_message(self, response) -> [dict]:
        append_message = []
        # 将当前用户输入和系统回复维护入chatgpt的session
        if response.get_content():
            append_message.append({"role": response.get_role(), "content": response.get_content()})

        if response.get_tool_calls():
            append_message.append({"role": response.get_role(),
                                   "tool_calls": [self.to_tool_call_dict(tool_call) for tool_call in
                                                  response.get_tool_calls()]})

        return append_message

    """
    将AGI TOOL Call 转化成 OpenAPI 支持的格式
    """

    def to_tool_call_dict(self, tool_call: AGIToolCall) -> dict:
        return {
            "id": tool_call.id,
            "type": tool_call.type,
            "function": {"name": tool_call.function.name,
                         "arguments": tool_call.function.arguments} if tool_call.function else None
        }

    def get_embeddings(self,texts,  model:str=None, dimensions=None):
        '''封装 OpenAI 的 Embedding 模型接口'''
        if model == "text-embedding-ada-002":
            dimensions = None
        if dimensions:
            data = self.client.embeddings.create(
                input=texts, model=model, dimensions=dimensions).data
        else:
            data = self.client.embeddings.create(input=texts, model=model).data
        return [x.embedding for x in data]

