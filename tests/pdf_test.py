import concurrent
import time
from concurrent.futures import (
    Future, ThreadPoolExecutor,
    as_completed, ProcessPoolExecutor
)

import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF

# const
RESOURCES_DIR = "pdf_resources/"

# 文本
text = "这是一个示例报告，包含扇形图和表格。"  # 默认不给用 Unicode。。。
text = "this is a sample report"


def draw_pie_chart():
    """ 绘制扇形图 """
    print("正在绘制扇形图...", flush=True)
    start_s = time.time()
    labels = ["A", "B", "C", "D"]
    sizes = [15, 30, 45, 10]
    colors = ["gold", "lightcoral", "lightskyblue", "yellowgreen"]
    explode = (0.1, 0, 0, 0)  # 仅 爆炸 A 片段

    plt.figure(figsize=(6, 4))
    plt.pie(sizes,
            explode=explode, labels=labels, colors=colors,
            autopct="%1.1f%%", shadow=True, startangle=140)
    plt.axis("equal")  # 等高宽比确保饼被画成圆形
    plt.title("Sample pie chart")  # （扇形图示例）中文会报错，应该是编码集的问题
    plt.savefig(RESOURCES_DIR + "pie_chart.png")  # 保存扇形图为图片
    plt.close()
    return f"draw_pie_chart completed(cost {time.time() - start_s:.6f} s)", None


def create_table():
    """ 创建和绘制表格 """
    print("正在绘制表格...", flush=True)
    start_s = time.time()
    data = {
        "project": ["A", "B", "C", "D"],  # 项目
        "value": [15, 30, 45, 10]  # 值
    }
    df = pd.DataFrame(data)
    # 创建一个新的图形
    fig, ax = plt.subplots(figsize=(6, 2))  # 设置图形大小
    ax.axis("tight")  # 关闭坐标轴
    ax.axis("off")  # 关闭坐标轴

    # 将 DataFrame 转换为表格
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

    # 设置表格样式
    table.auto_set_font_size(False)  # 关闭自动字体大小
    table.set_fontsize(12)  # 设置字体大小
    table.scale(1.2, 1.2)  # 设置表格缩放比例

    # 保存表格为图片
    plt.savefig(RESOURCES_DIR + "table_image.png", bbox_inches="tight", dpi=300)  # 保存为 PNG 图片
    plt.close()  # 关闭图形
    return f"create_table completed(cost {time.time() - start_s:.6f} s)", df


def footer(df):
    """ 将内容写入 PDF """
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.multi_cell(0, 10, "1 -> " + text)
    pdf.image(RESOURCES_DIR + "pie_chart.png", x=10, y=30, w=100)

    # pdf.multi_cell(0, 10, "2 -> " + text)
    # pdf.image(RESOURCES_DIR + "pie_chart.png", x=100, y=100, w=100)
    #
    # pdf.multi_cell(0, 10, "3 -> " + text)
    # pdf.image(RESOURCES_DIR + "pie_chart.png", x=100, y=170, w=100)

    # 添加表格
    pdf.ln(80)  # 空出一些空间
    pdf.set_font("Arial", size=12)
    pdf.cell(40, 10, "project", 1)
    pdf.cell(40, 10, "value", 1)
    pdf.ln()

    for index, row in df.iterrows():
        pdf.cell(40, 10, row["project"], 1)
        pdf.cell(40, 10, str(row["value"]), 1)
        pdf.ln()

    # 保存 PDF
    pdf.output(RESOURCES_DIR + "report.pdf")

    print("报告已生成，保存为 report.pdf")


if __name__ == '__main__':
    # (N)!: 多线程会出错：Process finished with exit code -1073741819 (0xC0000005)
    #   猜测可能是这个库压根不支持多线程，只能同步执行？
    #   错误代码 -1073741819 (或 0xC0000005) 通常表示访问冲突（Access Violation）
    #   这意味着程序试图访问未被允许的内存区域。这种错误在 Windows 系统中比较常见
    print(f"准备启动多进程（{time.time()}）", flush=True)
    with ProcessPoolExecutor(max_workers=3) as executor:
        print(f"启动了多进程（{time.time()}）", flush=True)
        futures = [
            executor.submit(fn)
            for fn in (
                draw_pie_chart,
                create_table,
            )
        ]
        df = None
        for future in as_completed(futures):
            msg, *res = future.result()
            print(msg, flush=True)
            if res:
                df, *_ = res
        print(f"全部运行完成（{time.time()}）", flush=True)
        footer(df)
