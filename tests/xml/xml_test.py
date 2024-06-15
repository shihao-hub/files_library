from xml.etree import ElementTree as et
from xml.dom import minidom

FILE_PATH = r"test.xml"

"""xml 相关内容
1. xml.etree.ElementTree -> 获得 ElementTree 类型，需要用 getroot() 函数获得根节点
2. xml.dom.minidom ->
3. ElementTree.Element -> [创建 XML 文件] 创建根节点 root，root.write 可将内容写入到文件中
3. minidom.Document -> [创建 XML 文件]
4. xml.etree.ElementTree -> [修改 XML 文件]
5. etree.XMLSchema -> [验证 XML 文件]
"""

"""xml 笔记
在 XML 技术中，标签属性所代表的信息，也可以被改成用子元素的形式来描述，例如：
    <input><name>text</name></input>
    Q: 我怎么知道标签属性用子元素的形式描述了呢？
"""


def get_namespaces(file_path):
    namespaces = {}

    # 使用 ElementTree 解析 XML 文件
    tree = et.parse(file_path)
    root = tree.getroot()

    # 获取默认命名空间
    default_namespace = root.tag.split('}')[0][1:]
    namespaces['default'] = default_namespace

    # 获取所有命名空间
    for elem in root.iter():
        namespace_uri, tag = et.QName(elem.tag).namespace, et.QName(elem.tag).localname
        if namespace_uri:
            namespaces[tag] = namespace_uri

    return namespaces


def et_method():
    tree = et.parse(FILE_PATH, parser=et.XMLParser())
    root = tree.getroot()

    # print(root.tag)
    # print(root.attrib)

    print(get_namespaces(FILE_PATH))

    # namespaces = {}
    # for e in root.attrib:
    #
    #
    # print([(e.tag, e.attrib) for e in tree.findall(".//person",namespaces=namespaces)])


def dom_method():
    dom = minidom.parse(FILE_PATH)
    elements = dom.getElementsByTagName("person")
    print([(e.tagName, e.childNodes) for e in elements])


if __name__ == '__main__':
    et_method()
    # dom_method()
