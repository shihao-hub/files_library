from xhtml2pdf import pisa

# HTML 内容
html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Test PDF</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a PDF generated from HTML.</p>
</body>
</html>
'''

# 将 HTML 转换为 PDF
with open('output.pdf', 'w+b') as pdf_file:
    pisa.CreatePDF(html_content, dest=pdf_file)
