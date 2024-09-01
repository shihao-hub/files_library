import collections
import pprint

import requests
from urllib import parse

DOMAIN = "https://www.bookstack.cn/"

MARKDOWNS = collections.OrderedDict([
    ("",""),
])

def main():
    # response = requests.get(parse.urljoin(DOMAIN, "/read/django-5.0-zh/6362c16a3dc5e894.md"))
    response = requests.get("https://www.programmercarl.com/%E6%95%B0%E7%BB%84%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80.html")
    # pprint.pprint(response.__dict__)
    response.encoding = "utf-8"
    pprint.pprint(response.text)


if __name__ == '__main__':
    main()
