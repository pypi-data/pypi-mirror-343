import json


class AGIUtil:

    # 一个辅助函数，只为演示方便，不必关注细节
    @staticmethod
    def format_json(data) -> str:

        def custom_serializer(obj):
            # 如果碰到特殊对象（如 ChatCompletionMessageToolCall），转为字符串或字典
            if hasattr(obj, "__dict__"):  # 尝试将对象转为字典
                return obj.__dict__
            else:
                return str(obj)  # 否则直接序列化为字符串

        """
        打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
        否则，直接打印该值。
        """
        if hasattr(data, 'model_dump_json'):
            data = json.loads(data.model_dump_json())

        if hasattr(data, 'to_dict'):
            data = data.to_dict()

        if (isinstance(data, (list, dict))):
            return (json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
                default=custom_serializer  # 使用自定义的序列化器
            ))
        else:
            return data

    @staticmethod
    def build_prompt(prompt_template, **kwargs):
        '''将 Prompt 模板赋值'''
        inputs = {}
        for k, v in kwargs.items():
            if isinstance(v, list) and all(isinstance(elem, str) for elem in v):
                val = '\n\n'.join(v)
            else:
                val = v
            inputs[k] = val
        return prompt_template.format(**inputs)