import re
import time
from datetime import datetime
import os
import zipfile
from tqdm import tqdm

base_file_path = r"D:\games\Steam\steamapps\common\Don't Starve Together\data\databundles"
file_path = os.path.join(base_file_path, "scripts.zip")

base_target_path = r"E:\ProgrammingProjects\IDEAProjects"
target_path = os.path.join(base_target_path, "zzz_scripts_" + datetime.now().strftime("%Y%m%d"))

time_s = time.time()
with zipfile.ZipFile(file_path) as zif_obj:
    members = None
    if members is None:
        members = zif_obj.namelist()

    for zipinfo in tqdm(members):
        zif_obj.extract(zipinfo, path=target_path, pwd=None)

    # zif_obj.extractall(path=target_path)
    print(f"解压成功，"
          f"压缩包共 {sum(info.file_size for info in zif_obj.infolist()) / 1024 / 1024:.2f} MB，"
          f"耗时 {time.time() - time_s:.2f} s")
