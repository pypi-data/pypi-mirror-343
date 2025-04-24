class AGIExtraParam:

    def __init__(self, client: "BaseAIClient"):
        self.temperature = client.default_temperature
        self.model = client.default_model
        self.parse_model = client.default_parse_model
        self.fc_model = client.default_fc_model
        self.tools = None
        self.stream = False

    def set_temperature(self, temperature: int):
        self.temperature = temperature
        return self

    def set_tools(self, tools: [dict, list[dict]]):
        self.tools = tools
        return self

    def set_model(self, model: str):
        self.model = model
        return self

    def set_parse_model(self, parse_model: str):
        self.parse_model = parse_model
        return self

    def set_stream(self, stream: bool):
        self.stream = stream
        return self

    """
    将对象的所有属性转换为字典表示。
    """

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "model": self.model,
            "tools": self.tools,
            "stream": self.stream
        }
