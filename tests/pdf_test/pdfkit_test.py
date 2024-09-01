import pdfkit

path_wkhtmltopdf = r"D:\software\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

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
pdfkit.from_string(html_content, 'output.pdf', configuration=config)

pdfkit.from_url('https://www.sohu.com/a/803390866_121860344', 'output2.pdf', configuration=config)
