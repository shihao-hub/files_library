import pprint

import fitz

IN_FILE_PATH = r"resources/out.pdf"


# IN_FILE_PATH = r"resources/PyQt5快速开发与实战电子书（1117）.pdf"

# def find_text_box(page: fitz.Page, text_to_delete):
#     # NOTE: 此处是在外面添加的，PyCharm 检测不到...
#     blocks = page.get_text("dict")["blocks"]
#     for block in blocks:
#         for line in block.lines:
#             for span in line.spans:
#                 text = span.text
#                 if text_to_delete in text:
#                     text = text.replace(text_to_delete, '')
#                 new_page.insert_text((span.rect[0], span.rect[1]), text)
#     return None


doc = fitz.open(IN_FILE_PATH)

page = doc[0]
text = page.get_text()
# print(type(find_text_box(page, "(PDFÑ¹ËõÆ÷ - Î´×¢²á°æ)\n")))
print(page.get_text_blocks())
print(f'text opt-"text": {page.get_text("text")}')  # （默认）带换行符的纯文本。无格式、无文字位置详细信息、无图像
print(f'text opt-"blocks": {page.get_text("blocks")}')  # 生成文本块（段落）的列表
print(f'text opt-"words": {page.get_text("words")}')  # 生成单词列表（不包含空格的字符串）
print(page.get_textbox(rect=(14.17300033569336, 11.225993156433105, 168.48104858398438, 30.50399398803711)))

# print(f'text opt-"html": {page.get_text("html")}')  # 创建页面的完整视觉版本，包括任何图像。这可以通过 internet 浏览器显示

# 与 HTML 相同的信息级别，但作为 Python 字典或 resp.JSON 字符串。
print(f'text opt-"dict": {pprint.pformat(page.get_text("dict")["blocks"][1])}')

# print(f'text opt-"json": {page.get_text("json")}')  #
# print(f'text opt-"rawdict": {page.get_text("rawdict")}')  # "dict"/"json" 的超级集合。它还提供诸如 XML 之类的字符详细信息。
# print(f'text opt-"rawjson": {page.get_text("rawjson")}')  #
# print(f'text opt-"xhtml": {page.get_text("xhtml")}')  # 文本信息级别与文本版本相同，但包含图像。
# print(f'text opt-"xml": {page.get_text("xml")}')  # 不包含图像，但包含每个文本字符的完整位置和字体信息。使用 XML 模块进行解释。

# print(f"页数 (int)：{doc.page_count}")
# print(f"元数据 (dict)：\n{pprint.pformat(doc.metadata)}")
# print(f"获取目录 (list)：{doc.get_outline_xrefs()}")

# NOTE: 页面处理是 MuPDF 功能的核心。
print(f"链接 links: {page.get_links()}")
print(f"注释 annots: {list(page.annots())}")
print(f"表单字段 widgets: {list(page.widgets())}")

pix = page.get_pixmap()
print(f"光栅图像 pixmap: {pix}")
pix.save(rf"resources/page-{page.number}.png")
