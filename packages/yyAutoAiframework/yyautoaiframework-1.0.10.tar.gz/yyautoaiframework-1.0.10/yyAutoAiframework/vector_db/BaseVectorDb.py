import re

from dotenv import load_dotenv, find_dotenv
# from nltk import sent_tokenize


class BaseVectorDb:
    def __init__(self):
        # 加载 .env 文件中定义的环境变量
        _ = load_dotenv(find_dotenv())

    def add_documents(self, documents):
         raise NotImplementedError("add_documents 方法需要子类实现")

    def search(self, query, top_n):
         raise NotImplementedError("search 方法需要子类实现")


    @staticmethod
    def split_text_zh(paragraphs, chunk_size=300, overlap_size=100):
        return BaseVectorDb.split_text(paragraphs, chunk_size, overlap_size,lang='zh')

    @staticmethod
    def overlap_text_zh(paragraphs, overlap_size=100):
        return BaseVectorDb.overlap_text(paragraphs, overlap_size,lang='zh')

    @staticmethod
    def overlap_text(paragraphs, overlap_size=100, lang='en'):

        chunks = []
        for index, paragraph in enumerate(paragraphs):
            chunk = paragraph
            prev_overlap_index = -1
            next_overlap_index = -1
            if index != 0:
                prev_overlap_index = index - 1
            if index != len(paragraphs) - 1:
                next_overlap_index = index + 1
            sentences = []
            if prev_overlap_index != -1:
                prev_overlap_paragraph = paragraphs[prev_overlap_index]
                # if lang == 'zh':
                #     sentences = [s.strip() for s in BaseVectorDb.sent_tokenize_zh(prev_overlap_paragraph)]
                # else:
                #     sentences = [s.strip() for s in sent_tokenize(prev_overlap_paragraph)]

                if len(sentences) > 0:
                    i = len(sentences)-1
                    overlap = ''
                    while i >= 0:
                        if len(sentences[i]) + len(overlap) <= overlap_size:
                            overlap = sentences[i] + ' ' + overlap
                            i -= 1
                        else:
                            break
                    chunk = overlap+chunk


            if next_overlap_index != -1:
                next_overlap_paragraph = paragraphs[next_overlap_index]
                if lang == 'zh':
                    sentences = [s.strip() for s in BaseVectorDb.sent_tokenize_zh(next_overlap_paragraph)]
                else:
                    sentences = [s.strip() for s in sent_tokenize(next_overlap_paragraph)]

                if len(sentences) > 0:
                    i = 0
                    overlap = ''
                    while i < len(sentences):
                        if len(sentences[i]) + len(overlap) <= overlap_size:
                            overlap = overlap+ ' ' + sentences[i]
                            i+=1
                        else:
                            break

                    chunk = chunk+overlap

            chunks.append(chunk)

        return chunks

    @staticmethod
    def split_text(paragraphs, chunk_size=300, overlap_size=100,lang='en'):
        '''按指定 chunk_size 和 overlap_size 交叠割文本'''
        sentences = []
        # if lang == 'zh':
        #     sentences = [s.strip() for p in paragraphs for s in BaseVectorDb.sent_tokenize_zh(p)]
        # else:
        #     sentences = [s.strip() for p in paragraphs for s in sent_tokenize(p)]
        chunks = []
        i = 0
        while i < len(sentences):
            chunk = sentences[i]
            overlap = ''
            prev_len = 0
            prev = i - 1
            # 向前计算重叠部分
            while prev >= 0 and len(sentences[prev]) + len(overlap) <= overlap_size:
                overlap = sentences[prev] + ' ' + overlap
                prev -= 1
            chunk = overlap + chunk
            next = i + 1
            # 向后计算当前chunk
            while next < len(sentences) and len(sentences[next]) + len(chunk) <= chunk_size:
                chunk = chunk + ' ' + sentences[next]
                next += 1
            chunks.append(chunk)
            i = next
        return chunks

    def sent_tokenize_zh(input_string):
        """按标点断句"""
        # 按标点切分
        sentences = re.split(r'(?<=[。！？；?!])', input_string)
        # 去掉空字符串
        return [sentence for sentence in sentences if sentence.strip()]