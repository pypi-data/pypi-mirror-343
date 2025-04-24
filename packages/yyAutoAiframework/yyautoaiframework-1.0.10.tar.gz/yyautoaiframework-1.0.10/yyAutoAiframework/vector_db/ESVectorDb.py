import os
import time
import warnings

from elasticsearch7 import Elasticsearch, helpers

from yyAutoAiframework.util.RagUtil import RagUtil
from yyAutoAiframework.vector_db.BaseVectorDb import BaseVectorDb


class ESVectorDb(BaseVectorDb):
    def __init__(self, collection_name, embedding_fn):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 引入配置文件
        ELASTICSEARCH_BASE_URL = os.getenv('ELASTICSEARCH_BASE_URL')
        ELASTICSEARCH_PASSWORD = os.getenv('ELASTICSEARCH_PASSWORD')
        ELASTICSEARCH_NAME = os.getenv('ELASTICSEARCH_NAME')
        # 初始化 OpenAI 客户端
        # tips: 如果想在本地运行，请在下面一行 print(ELASTICSEARCH_BASE_URL) 获取真实的配置

        # 1. 创建Elasticsearch连接
        es = Elasticsearch(
            hosts=[ELASTICSEARCH_BASE_URL],  # 服务地址与端口
            http_auth=(ELASTICSEARCH_NAME, ELASTICSEARCH_PASSWORD),  # 用户名，密码
        )
        self.embedding_fn = embedding_fn

        # 3. 如果索引已存在，删除它（仅供演示，实际应用时不需要这步）
        if not es.indices.exists(index=collection_name) :
            es.indices.create(index=collection_name)

        self.instance = es
        self.collection = collection_name
        warnings.simplefilter("ignore")  # 屏蔽 ES 的一些Warnings

    """
    初始化ES 数据
    """
    def add_documents(self,documents):
        es = self.instance
        # 5. 灌库指令
        actions = [
            {
                "_index": self.collection,
                "_source": {
                    "keywords": self.embedding_fn(para),
                    "text": para
                }
            }
            for para in documents
        ]
        helpers.bulk(es, actions)
        time.sleep(2)


    """
    执行ES 查询
    """
    def search(self,query_string,top_n=3):
        es = self.instance
        # ES 的查询语言
        search_query = {
            "match": {
                "keywords": RagUtil.to_keywords(query_string)
            }
        }
        res = es.search(index=self.collection, query=search_query, size=top_n)
        print(res)
        results =  [hit["_source"]["text"] for hit in res["hits"]["hits"]]
        for r in results:
            print("ES 查询结果："+r + "\n")
        return results