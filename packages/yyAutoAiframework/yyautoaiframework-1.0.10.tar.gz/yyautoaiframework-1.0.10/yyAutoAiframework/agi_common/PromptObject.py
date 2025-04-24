class PromptObject:
    def __init__(self, context, instruction, output_format, example):
        """
        初始化 PromptObject 对象
        :param context: 任务的上下文说明
        :param instruction: 具体的任务说明
        :param output_format: 输出格式的要求
        :param examples: 示例数据，用来辅助任务理解
        """
        self.context = context
        self.instruction = instruction
        self.output_format = output_format
        self.example = example
