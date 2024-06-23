import pangu

text = """
如果在Bootstrap创建的网页开头不使用HTML5的文档类型（Doctype），
您可能会面临一些浏览器显示不一致的问题，甚至可能面临一些特定情境下的不一致，以致于您的代码不能通过W3C标准的验证。
"""

space_text = pangu.spacing_text(text)
print(space_text)
