import fitz
from pymupdf import Pixmap

IN_FILE_PATH = r"resources/PyQt5快速开发与实战电子书（1117）.pdf"

doc = fitz.open(IN_FILE_PATH)
tmp_doc = fitz.open()
text_to_delete = "(PDFÑ¹ËõÆ÷ - Î´×¢²á°æ)\n"

images = None

for i, page in enumerate(doc):
    # if i != 0 and i % 100 == 0:
    #     tmp_doc.save(rf"resources/out{int(i / 100)}.pdf")
    #     tmp_doc.close()
    #     tmp_doc = fitz.open()
    if i == 10:
        break
    print(f"正在处理第 {i} 页")
    blocks = page.get_text("dict")["blocks"]
    tmp_page = tmp_doc.new_page(-1, width=page.rect.width, height=page.rect.height)
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
        images = images or sorted(page.get_images(full=True))
        # print([images[i][0] for i in range(20)])
        # print(f"images len: {len(images)}")
        img = images[i]
        image_info = page.get_image_info(img[0])
        tmp_page.insert_image(image_info[0]['bbox'], pixmap=Pixmap(doc, img[0]))

del images
try:
    tmp_doc.save(r"resources/out2.pdf")
    tmp_doc.close()
except Exception as e:
    print(e)
