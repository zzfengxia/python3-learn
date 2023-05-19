import PyPDF2
import pdfplumber
import re

"""
使用anaconda Prompt安装PyPDF2库，`pip install PyPDF2`
`pip install pdfplumber`安装pdfplumber库，pdfplumber提供了更高级的功能
"""


class PDFUtil(object):
    def __init__(self, path):
        self.file_path = path

    def read_by_pypdf2(self, from_page=0, to_page=-1):
        # 打开 PDF 文件
        with open(self.file_path, 'rb') as file:
            # 创建一个 PDF Reader 对象
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f'文件共有{num_pages}页')

            to_page = num_pages if to_page == -1 else to_page
            # 提取每一页的文本内容，这里输出时先输出了该页所有标题，再输出的内容
            for page_num in range(num_pages):
                if from_page <= page_num < to_page:
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    print(text)

    """
    解析中文可能出现cid:xxx的情况
    """
    def parse_to_markdown_code(self, page_text):
        num_pages = len(page_text)

        is_inline = False
        new_inline = False
        pattern = r'^\d+\.'  # 匹配标题，以“数字+.”开头
        for page_num in range(num_pages):
            # lines = pdf.pages[page_num].extract_text_lines()

            # 行数据各字段含义，以下是部分字段说明
            # "text"：表示文本行的内容。
            # "x0"：表示文本行左侧的x坐标。
            # "y0"：表示文本行底部的y坐标。
            # "x1"：表示文本行右侧的x坐标。
            # "y1"：表示文本行顶部的y坐标。
            # for line in lines:
            # 输出页面内容
            #    print(line)

            # 原样输出
            text = page_text[page_num]
            # 按行解析文本
            lines = text.splitlines()

            for line in lines:
                if re.match(pattern, line.strip()):
                    if is_inline:
                        print("```")
                        print("\n")
                    # 标题
                    print(re.sub(pattern, "## ", line))
                    is_inline = True
                    new_inline = True
                    continue
                if new_inline:
                    print("```shell")
                    print(line)
                    new_inline = False
                    continue
                if is_inline and not new_inline:
                    print(line)
                    continue

    def read_by_pdfplumber(self, from_page=0, to_page=-1, parse_fun=None):
        with pdfplumber.open(self.file_path) as pdf:
            num_pages = len(pdf.pages)
            to_page = num_pages if to_page == -1 else to_page
            page_text = []
            for page_num in range(num_pages):
                if page_num > to_page:
                    break
                if from_page <= page_num < to_page:
                    # lines = pdf.pages[page_num].extract_text_lines()

                    # 原样输出
                    text = pdf.pages[page_num].extract_text_simple()
                    page_text.append(text)

            if parse_fun is not None:
                parse_fun(page_text)
                return

            for p in page_text:
                print(p)
    """
    pdf格式的api文档解析为java实体类
    """
    def api_to_entity(self):
        # no op
        return


if __name__ == '__main__':
    pdfUtil = PDFUtil("D:\\qiyu-work\\文档\\UNIT网站功能API文档-20210621.pdf")
    #pdfUtil = PDFUtil("D:\\mycode\\daily-note\\资料书\\【实用】279个开箱即用的shell脚本.pdf")
    pdfUtil.read_by_pdfplumber(from_page=10, to_page=11)
