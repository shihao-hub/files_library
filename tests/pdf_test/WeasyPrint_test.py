from weasyprint import HTML

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

# 转换为 PDF
HTML(string=html_content).write_pdf('output.pdf')
