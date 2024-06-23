import re

with open(r"C:\Users\29580\Desktop\markdowns\git_push.bat", "r+", encoding="utf-8") as file:
    content = file.read()
    file.seek(0)

    content = re.compile(r"echo ").sub("", content)
    print(content)
    file.write(content)
