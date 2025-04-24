import logging

from yyAutoAiframework.util.AGIUtil import AGIUtil
from yyAutoAiframework.vector_db import BaseVectorDb

# from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

class RagBotComponent:
    model = None
    def __init__(self, vector_db:BaseVectorDb, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results

    def chat(self, user_query):
        # 1. 检索
        # search_results = self.vector_db.search(user_query, self.n_results*2)
        # print("search_results:"+AGIUtil.format_json(search_results))
        # if not RagBotComponent.model:
        #     print("加载模型...")
        #     model = CrossEncoder('BAAI/bge-reranker-large', max_length=512,device='cuda' if torch.cuda.is_available() else 'cpu')  # 多语言，国产，模型较大
        #     RagBotComponent.model = model
        #     print("加载模型结束...")
        #
        # scores = RagBotComponent.model.predict([(user_query, doc)
        #                         for doc in search_results])
        # sorted_list = sorted(
        #     zip(scores, search_results), key=lambda x: x[0], reverse=True)
        #
        # sorted_search_results = [doc for _, doc in sorted_list[:self.n_results]]
        #
        # print("sorted_search_results:"+AGIUtil.format_json(sorted_search_results))

        search_results = self.vector_db.search(user_query, self.n_results)
        logger.info("search_results:" + AGIUtil.format_json(search_results))
        sorted_search_results = search_results
        # 2. 构建 Prompt
        prompt_template = """
                    你是一个问答机器人。
                    你的任务是根据下述给定的已知信息回答用户问题。

                    已知信息:
                    {context}

                    用户问：
                    {query}

                    如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
                    请不要输出已知信息中不包含的信息或答案。
                    请用中文回答用户问题。
                    """

        prompt = AGIUtil.build_prompt(
            prompt_template, context=sorted_search_results, query=user_query)

        # 3. 调用 LLM
        logger.info("开始调用LLM:")
        response = self.llm_api(prompt)
        return response