import os

import chromadb
from chromadb import Settings

from yyAutoAiframework.vector_db.BaseVectorDb import BaseVectorDb


class ChromaVectorDb(BaseVectorDb):
    __chroma_client = None
    def __init__(self, collection_name, embedding_fn):
        # 加载 .env 文件中定义的环境变量
        super().__init__()
        # 获取环境变量并提供默认值
        __host_value = os.getenv("CHROME_DB_HOST")
        __port_value = int(os.getenv("CHROME_DB_PORT"))

        # chroma_client = chromadb.Client(Settings(allow_reset=True))
        if ChromaVectorDb.__chroma_client is None:
            ChromaVectorDb.__chroma_client = chromadb.HttpClient(host= __host_value, port=__port_value,settings=Settings(allow_reset=False))

        # 创建一个 collection
        self.collection = ChromaVectorDb.__chroma_client.get_or_create_collection(
            name=collection_name)
        self.embedding_fn = embedding_fn
        self.client = ChromaVectorDb.__chroma_client

    def add_documents(self, file_name,documents):
        import hashlib
        # 创建md5对象
        md5_obj = hashlib.md5()
        # 更新对象的字符串
        md5_obj.update(file_name.encode('utf-8'))  # 将字符串编码为UTF-8字节串
        # 获取16进制表示的哈希值
        file_name_md5_hash = md5_obj.hexdigest()
        print("MD5加密结果：", file_name_md5_hash)
        '''向 collection 中添加文档与向量'''
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[file_name_md5_hash+f"id{i}" for i in range(len(documents))]  # 每个文档的 id
        )

    def search(self, query, top_n=3):
        '''检索向量数据库'''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        # print(AGIUtil.format_json(results))
        return results['documents'][0]

    def delete_documents_by_ids(self, ids):
        '''删除向量数据库'''
        self.collection.delete(ids=ids)

    def get_documents_count(self):
        '''获取向量数据库'''
        return self.collection.count()

    def get_all_documents(self):
        '''获取向量数据库'''
        return self.collection.get()

    def get_documents_by_ids(self,ids):
        '''获取向量数据库'''
        return self.collection.get(ids)

    def delete_all_documents(self):
        '''获取向量数据库'''
        return self.client.delete_collection(name=self.collection.name)
