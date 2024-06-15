# 常见的英、美等国的英文缩写
from pydoc import html

import requests, bs4


def process_data() -> dict:
    data = {}
    filename = "abbreviation.html"
    file = open(filename, "r", encoding="utf-8")
    bs4_obj = bs4.BeautifulSoup(file, features="html.parser")
    file.close()
    print(type(bs4_obj))
    elms = bs4_obj.select("p")
    print(len(elms))
    for i in range(0, len(elms), 2):
        # 这个 split 似乎不支持正则表达式？
        print(elms[i].getText().split("="))
    return data


def main():
    process_data()


if __name__ == "__main__":
    main()
