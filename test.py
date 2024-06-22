import pprint

import fitz
from pymupdf import Pixmap

IN_FILE_PATH = r"resources/out.pdf"


def delete_text_from_page(doc, page_number, text_to_delete):
    page: fitz.Page = doc[page_number]

    blocks = page.get_text("dict")["blocks"]

    tmp_doc = fitz.open()
    tmp_page = tmp_doc.new_page(-1, width=page.rect.width, height=page.rect.height)

    pprint.pprint(blocks)
    for block in blocks:
        try:
            for line in block.lines:
                for span in line.spans:
                    text = span.text
                    if text_to_delete in text:
                        text = text.replace(text_to_delete, '')
                    tmp_page.insert_text((span.bbox[0], span.bbox[1]), text)
        except AttributeError as e:
            if not e.args[0] == "'dict' object has no attribute 'lines'":
                raise

    # 将原始页面上的图像和矢量图形复制到临时页面
    for img in page.get_images(full=True):
        # print(img)
        image_info = page.get_image_info(img[0])
        # print(image_info)
        tmp_page.insert_image(image_info[0]['bbox'],pixmap=Pixmap(doc, img[0]))
        break

    # 将临时页面的内容复制回原始文档的页面
    # page.set_cropbox(page.rect)  # 重置裁剪框
    # page.insert_pdf(tmp_doc, from_page=0, to_page=-1)  # 插入修改后的内容

    # 关闭临时文档
    tmp_doc.save(r"resources/out2.pdf")
    tmp_doc.close()

# 2024-06-22：
#   1. page.get_images(full=True) 有问题，长度为 570，正好等于页数
#   但是这个明明是调用的是 page 啊...
#   2. 找一下页面压缩的函数
#   3. 确实可以实现文本替换，但是稍微有点复杂，而且各个版本区别太大，找资料也很麻烦...可恶...

doc = fitz.open(IN_FILE_PATH)
delete_text_from_page(doc, 0, "(PDFÑ¹ËõÆ÷ - Î´×¢²á°æ)\n")
