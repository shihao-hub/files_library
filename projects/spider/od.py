import os

import requests
import webbrowser

# url = "https://blog.csdn.net/banxia_frontend/article/details/134450561"
# webbrowser.open(url)


url = "https://blog.csdn.net/banxia_frontend/article/details/134450561"
url = "https://cn.bing.com/"
url = "https://blog.csdn.net/banxia_frontend/article/details/134727359?spm=1001.2014.3001.5502"
url = "https://www.csdn.net/?spm=1001.2101.3001.4476"
page = 1

response = requests.get(url)
print(response)

response.raise_for_status()

os.makedirs("od", exist_ok=True)
with open("od/od_" + str(page) + ".html", "w", encoding="utf-8") as file:
    # file.write(response.text)
    print(len(response.text))
