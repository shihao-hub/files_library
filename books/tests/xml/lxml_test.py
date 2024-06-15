from lxml import etree
from lxml.etree import _Element

text = """\
<person name="abc">
    <name>John</name>
    <age>30</age>
    <city>New York</city>
</person>
"""

xml: _Element = etree.fromstring(text, etree.XMLParser())

# print([e for e in dir(xml) if not e.startswith("__") or not e.endswith("__")])

# print(f"attrib: {xml.attrib}")
# print(f"base: {xml.base}")
# print(f"nsmap: {xml.nsmap}")
# print(f"prefix: {xml.prefix}")
# print(f"sourceline: {xml.sourceline}")
# print(f"tag: {xml.tag}")
# print(f"tail: {xml.tail}")
# print(f"text: {xml.text}")


elements = xml.xpath("//name")
print([e.tag for e in elements])

for e in xml.iter():
    print(e)
