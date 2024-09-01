from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def create_pdf(filename):
    """ 创建一个 PDF 文件 """
    pdfmetrics.registerFont(TTFont("SimSun", "SimSun.ttf"))

    # 创建一个 Canvas 对象
    c = canvas.Canvas(filename, pagesize=letter)

    # 设置字体
    c.setFont("SimSun", 12)

    # 添加文本
    c.drawString(100, 750, "Hello, ReportLab!你好！")
    c.drawString(100, 730, "This is a simple PDF document.")

    # 绘制一个矩形
    c.rect(100, 650, 400, 50, fill=1)  # fill=1 表示填充

    # 添加更多文本
    c.setFillColor("white")  # 设置填充颜色为白色
    c.drawString(110, 650, "This rectangle is filled with color.")

    # 完成并保存 PDF 文件
    c.save()


if __name__ == '__main__':
    # 调用函数创建 PDF
    create_pdf("example.pdf")
