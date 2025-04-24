import re

import numpy as np
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
from numpy import dot
from numpy.linalg import norm


class RagUtil:
    # # 实验室平台已经内置
    # nltk.download('punkt')  # 英文切词、词根、切句等方法
    # nltk.download('stopwords')  # 英文停用词库
    # nltk.download('punkt_tab')

    @staticmethod
    def to_keywords(input_string):
        '''（英文）文本只保留关键字'''
        # 使用正则表达式替换所有非字母数字的字符为空格
        # no_symbols = re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
        # word_tokens = word_tokenize(no_symbols)
        # # 加载停用词表
        # stop_words = set(stopwords.words('english'))
        # ps = PorterStemmer()
        # 去停用词，取词根
        # filtered_sentence = [ps.stem(w)
        #                      for w in word_tokens if not w.lower() in stop_words]
        filtered_sentence = []
        return ' '.join(filtered_sentence)
    @staticmethod
    def cos_sim(a, b):
        '''余弦距离 -- 越大越相似'''
        return dot(a, b) / (norm(a) * norm(b))
    @staticmethod
    def l2(a, b):
        '''欧氏距离 -- 越小越相似'''
        x = np.asarray(a) - np.asarray(b)
        return norm(x)