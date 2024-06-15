import os

for path, dirs, files in os.walk(r"C:\Users\29580\Documents\Klei\DoNotStarveTogether\1255361974"):
    for filename in files:
        if filename == "modoverrides.lua":
            file_path = os.path.join(path, filename)
            with open(file_path, "r", encoding="utf-8") as fr:
                content = fr.read()
                if "1909182187" in content:
                    with open(filename, "w", encoding="utf-8") as fw:
                        fw.write(content)
                    break
