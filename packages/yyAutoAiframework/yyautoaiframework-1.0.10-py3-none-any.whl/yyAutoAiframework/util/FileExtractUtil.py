import io
import re

import pandas as pd
import pdfplumber
from PIL import Image
from pdfminer.converter import PDFPageAggregator
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LAParams, LTImage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class FileExtractUtil:

    @staticmethod
    def extract_text_from_pdf_miner(filename, page_numbers=None, min_line_length=1):
        '''从 PDF 文件中（按指定页码）提取文字'''
        paragraphs = []
        full_text = ''
        # 提取全部文本
        for i, page_layout in enumerate(extract_pages(filename)):
            buffer = ''
            # 如果指定了页码范围，跳过范围外的页
            if page_numbers is not None and i not in page_numbers:
                continue
            for element in page_layout:
                # print("是否TextContainer:%s,是否是LTRect:%s" % (isinstance(element, LTTextContainer),isinstance(element, LTRect)))
                if isinstance(element, LTTextContainer) :
                    element_text = element.get_text().strip().replace('\n', '')
                    # print("element_text:" + element_text)
                    if len(element_text) >= min_line_length:
                        buffer += (' '+element_text) if not element_text.endswith('-') else element_text.strip('-')



            #将此页的数据加入集合中
            if buffer:
                paragraphs.append(buffer)

        #打印前4段
        # for para in paragraphs:
        #     print("pdf 解析："+para + "\n")

        return paragraphs

    @staticmethod
    def remove_table_from_text(text_str:str, tables):
        for table in tables:
            if (len(table[1:])>1 or len(table[1:]) ==1 and table[1:][0][0]!="") and table[0] is not None and table[-1] is not None:
                first_row = ' '.join([str(item) if item is not None else '' for item in table[0]])
                last_row = ' '.join([str(item) if item is not None else '' for item in table[-1]])
                if len(last_row) >20:
                    # 截取Last_row 的前10个字+Last_row 的后10个字
                    last_row_part1 = last_row[:10].strip()
                    last_row_part2 = last_row[-10:].strip()
                    # 从文本中移除表格内容
                    pattern = re.escape(first_row)+r"[\s\S]*?"+re.escape(last_row_part1)+r"[\s\S]*?"+re.escape(last_row_part2)+""
                    text_str = re.sub(pattern, '', text_str, flags=re.DOTALL)
                else:
                    # 从文本中移除表格内容
                    pattern = re.escape(first_row)+r"[\s\S]*?"+re.escape(last_row)
                    text_str = re.sub(pattern, '', text_str, flags=re.DOTALL)

            # 将表格数据转换为字符串
            # table_str = '\n'.join(['\t'.join(row) for table in tables for row in table]
        return text_str

    @staticmethod
    def extract_text_from_pdf_plumber(filename, page_numbers=None, min_line_length=1):
        paragraphs = []
        with pdfplumber.open(filename) as pdf:
            for page in pdf.pages:
                buffer = ''
                # 如果指定了页码范围，跳过范围外的页
                if page_numbers is not None and page.page_number not in page_numbers:
                    continue
                element_text = page.extract_text()  # 提取纯文本
                tables = page.extract_tables()  # 提取表格
                if len(element_text) >= min_line_length:
                    append_str = FileExtractUtil.remove_table_from_text(element_text, tables)
                    append_str = re.sub(r'[\t ]', '', append_str)
                    buffer += (' ' + append_str+ "\n") if not append_str.endswith('-') else append_str.strip('-')
                for table in tables:
                    if len(table[1:])>1 or len(table[1:]) ==1 and table[1:][0][0]!="":
                        df = pd.DataFrame(table[1:], columns=table[0])
                        table_text = df.to_string()
                        if len(table_text) >= min_line_length:
                            buffer += (' ' + table_text+ "\n") if not table_text.endswith('-') else table_text.strip('-')

                # 将此页的数据加入集合中
                if buffer:
                    paragraphs.append(buffer)
        # #打印前4段
        for para in paragraphs:
            print("pdf 解析4："+para + "\n")

        return paragraphs

    # @staticmethod
    # def extract_table_from_pdf(filename, page_numbers=None):
    #     tables = tabula.read_pdf(filename, pages="all")
    #     for df in tables:
    #         print(df)

    """
    暂时不使用
    """
    @staticmethod
    def extract_image_from_pdf(filename):
        '''从 PDF 文件中提取图像'''
        image_info = []
        resource_manager = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)

        with open(filename, 'rb') as fp:
            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
                layout = device.get_result()
                for lt_obj in layout:
                    if isinstance(lt_obj, LTImage):
                        image_info.append({
                            'page_number': page.pageid,
                            'x0': lt_obj.x0,
                            'y0': lt_obj.y0,
                            'x1': lt_obj.x1,
                            'y1': lt_obj.y1,
                            'width': lt_obj.width,
                            'height': lt_obj.height,
                            'stream': lt_obj.stream
                        })

        return image_info


    """
    暂时不使用
    """
    @staticmethod
    def save_images_from_pdf(filename, output_folder):
        '''从 PDF 文件中提取图像并保存到指定文件夹'''
        import os
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = FileExtractUtil.extract_image_from_pdf(filename)
        for i, image in enumerate(images):
            stream = image['stream']
            file_ext = stream.get_ext()
            if file_ext in ['.jpg', '.jpeg']:
                img = Image.open(io.BytesIO(stream.get_rawdata()))
                img.save(os.path.join(output_folder, f'image_{i+1}.jpg'))
            elif file_ext == '.png':
                img = Image.open(io.BytesIO(stream.get_rawdata()))
                img.save(os.path.join(output_folder, f'image_{i+1}.png'))
            # 可以添加更多文件格式的支持

        return images