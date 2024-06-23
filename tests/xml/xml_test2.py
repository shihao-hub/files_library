import pprint

import lxml
import lxml.etree as ET
from lxml.etree import _Element as Element
from typing import List

xml_data = '''\
<bookstore>
    <book category="COOKING">
        <title lang="en">Everyday Italian</title>
        <author>Giada De Laurentiis</author>
        <year>2005</year>
        <price>30.00</price>
    </book>
    <book category="CHILDREN">
        <title lang="en">Harry Potter</title>
        <author>J K. Rowling</author>
        <year>2005</year>
        <price>29.99</price>
    </book>
    <book category="WEB">
        <title lang="en">Learning XML</title>
        <author>Erik T. Ray</author>
        <year>2003</year>
        <price>39.95</price>
    </book>
</bookstore>
'''

root: Element = ET.fromstring(xml_data)

book_titles: List[Element] = root.xpath('/bookstore/book/title')  # /bookstore/book[@category="WEB"]/title
for e in book_titles:
    # pprint.pprint(dir(e))
    print(list(e.iterchildren()))
    print(e.getchildren())
    print(e.attrib)
    print(e.tag)
    print(e.text, type(e.text))
    print(e.nsmap)
    print()
    break

# book_title = root.find('title').text
# book_author = root.find('author').text
# book_genre = root.find('genre').text
# book_price = float(root.find('price').text)
#
# print(f"Book: {book_title}, Author: {book_author}, Genre: {book_genre}, Price: {book_price}")
