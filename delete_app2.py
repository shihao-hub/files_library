import fitz


def cover_text_with_image(page, text_area, image_path):
    # 计算文本区域的边界
    x0, y0, x1, y1 = text_area

    # 打开图片文件
    img_document = fitz.open(image_path)  # 打开图片
    img_page = img_document[0]  # 第一页
    img = img_page.get_pixmap()  # 获取图片的像素图

    # 将图片插入到PDF页面
    img_inserted = page.insert_image(img)  # 插入图片
    # img_inserted.insert_text((x0, y0), "", align=1)  # 在图片位置上插入文本（这里是空文本）

    # 将图片作为覆盖层添加到页面
    page.insert_image(img_inserted, x0, y0, width=img.width, height=img.height)


# 打开PDF文件
pdf = fitz.open(r"resources/out.pdf")

# 选择页面
page = pdf[0]  # 第一页

# 要覆盖的文本区域（这里需要您根据实际情况指定坐标）
text_area = (14.17300033569336, 11.225993156433105, 168.48104858398438, 30.50399398803711)  # 示例坐标

# 覆盖图片的路径
image_path = r"resources/img.png"  # 这里需要提供图片的路径

# 覆盖文本
cover_text_with_image(page, text_area, image_path)

# 保存修改后的PDF
pdf.save(r"resources/out2.pdf")

# 关闭PDF文件
pdf.close()
