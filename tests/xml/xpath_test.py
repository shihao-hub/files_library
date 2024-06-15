from lxml import etree

text = """
<html><body><div>
    <ul>
        <li class="item-0"><a href="link1.html"><p>first item</p></a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-inactive">111<a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">forth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a>
        </li>
    </ul>
</div>
</body></html>
"""

html = etree.HTML(text, etree.HTMLParser())
# print(html.xpath('//li[@class="item-0"]/text()'))
# print(html.xpath('//li[@class="item-0"]/a/text()'))
# print(html.xpath('//li[@class="item-0"]//text()'))
# print(html.xpath('//li[@class="item-0"]/..//text()'))
print(html.xpath('//li/a/@href'))
# print(html.xpath('//li/following::*[1]'))
print(type(html.xpath('//li[@class="item-inactive"]')[0]))

element: etree._Element = html.xpath('//li[@class="item-inactive"]')[0]
print(etree.tostring(element))
print(element.get("class"))
print(list(map(etree.tostring, element.iter())))
print(element.text)
