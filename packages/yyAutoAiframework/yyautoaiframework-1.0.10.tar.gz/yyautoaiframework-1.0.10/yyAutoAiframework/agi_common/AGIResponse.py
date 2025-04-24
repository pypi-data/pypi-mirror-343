class AGIToolFunction:
    def __init__(self, name, arguments):
        self.arguments = arguments
        self.name = name

    def set_arguments(self, arguments):
        self.arguments = arguments
        return self

    def to_dict(self):
        return {
            "name": self.name,
            "arguments": self.arguments,
        }


class AGIToolCall:
    def __init__(self, id: str, type: str, function: AGIToolFunction = None):
        self.id = id
        self.type = type
        self.function = function

    def set_function(self, function: AGIToolFunction):
        self.function = function
        return self

    def get_function(self):
        return self.function

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "function": self.function.to_dict() if self.function else None,
        }


class StreamResponse:
    def __init__(self, stream_content):
        self.stream_content = stream_content

    def set_stream_content(self, stream_content):
        self.stream_content = stream_content
        return self

    def to_dict(self):
        return {
            "stream_content": self.stream_content
        }


class AGIResponse:

    def __init__(self):
        self.content = None,
        self.tool_calls = None
        self.role = None
        self.stream_response = None

    def set_content(self, content):
        self.content = content
        return self

    def set_tool_calls(self, tool_calls: AGIToolCall):
        if isinstance(tool_calls, list):
            self.tool_calls = tool_calls  # 设置为列表
        else:
            self.tool_calls.append(tool_calls)  # 单个添加到列表
        return self

    def set_role(self, role):
        self.role = role
        return self

    def set_stream_response(self, stream_response: StreamResponse):
        if isinstance(stream_response, list):
            self.stream_response = stream_response  # 设置为列表
        else:
            self.stream_response.append(stream_response)  # 单个添加到列表
        return self

    def get_content(self):
        return self.content

    def get_tool_calls(self):
        return self.tool_calls

    def get_role(self):
        return self.role

    def get_stream_response(self):
        return self.stream_response

    def to_dict(self):
        return {
            "content": self.content,
            "tool_calls": [tool_call.to_dict() for tool_call in self.tool_calls] if self.tool_calls else None,
            "role": self.role,
            "stream_response": self.stream_response,
        }
