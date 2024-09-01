from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def create_pie_chart(drawing, data, width, height, horizontal=False, index=0):
    pie = Pie()

    if horizontal:
        pie.x = 0 + index * 175
        pie.y = 0
    else:
        pie.x = 0
        pie.y = 0

    pie.width = width
    pie.height = height
    pie.data = data
    pie.labels = [f"{d}%" for d in data]
    pie.slices.strokeWidth = 0.5
    pie.slices[0].fillColor = colors.red
    pie.slices[1].fillColor = colors.green
    pie.slices[2].fillColor = colors.blue
    pie.slices[3].fillColor = colors.orange
    pie.slices[4].fillColor = colors.yellow

    drawing.add(pie)


def create_pdf(filename):
    # 注册字体
    pdfmetrics.registerFont(TTFont("SimSun", "SimSun.ttf"))

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    # 设置中文字体
    styles['Normal'].fontName = 'SimSun'
    story = []

    for i in range(3):
        story.extend([Paragraph(f"这是第 {i + 1} 行文本", styles['Normal']), Spacer(1, 24)])

        # 添加三个扇形图
        width, height = 1.5 * inch, 1.5 * inch

        drawing = Drawing(width, height)
        create_pie_chart(drawing, [30, 30, 40], width, height, True, 0)
        create_pie_chart(drawing, [20, 50, 30], width, height, True, 1)
        create_pie_chart(drawing, [25, 25, 25, 25], width, height, True, 2)
        story.append(drawing)
        story.append(Spacer(1, 24))
    story.extend([Paragraph(f"这是第 {4} 行文本", styles['Normal']), Spacer(1, 24)])


    story.append(Spacer(1, 24))
    # 创建表格
    data = [
        ['名称', '数量', '价格', "  ", "  ", "  ", "  ", "  ", "  ", ],
        ['商品A', '10', '$100', "  ", "  ", "  ", "  ", "  ", "  ", ],
        ['商品B', '20', '$200', "  ", "  ", "  ", "  ", "  ", "  ", ],
        ['商品C', '30', '$300', "  ", "  ", "  ", "  ", "  ", "  ", ]
    ]

    table = Table(data, colWidths=[0.8 * inch for _ in range(len(data[0]))])
    # 设置表格样式
    #   TableStyle 中的元组用于定义表格的样式，每个元组都包含四个元素，分别代表样式的属性、开始位置、结束位置和对应的值。
    #   开始位置（Start Cell）：这是一个元组，指定样式应用的开始单元格，格式为 (列索引, 行索引)。
    #                          索引从 0 开始。例如，(0, 0) 表示第一列第一行。
    table.setStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # 表头背景颜色
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # 表头字体颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 内容居中对齐
        ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 设置表头字体
        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 设置单元格字体
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头底部填充
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # 表格内容背景颜色
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 表格边框
    ])

    story.append(table)

    # 生成 PDF
    doc.build(story)


if __name__ == '__main__':
    # 创建 PDF 文件
    create_pdf("report.pdf")
