import pprint
import re

import bs4

text = """\
<title>Title</title>
<p>Hello</p>
<p>Hello1</p>
"""

soup = bs4.BeautifulSoup(text, "lxml")

# pprint.pprint(soup.__dict__)

print(soup.title.string)
print(list(soup.p.strings))
print(list(map(type, soup.find_all(string=re.compile(r"Hello")))))
bs4.element.NavigableString