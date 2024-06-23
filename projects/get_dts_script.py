import re
from datetime import datetime
import os
import zipfile

base_file_path = r"D:\games\Steam\steamapps\common\Don't Starve Together\data\databundles"
file_path = os.path.join(base_file_path, "scripts.zip")

base_target_path = r"E:\ProgrammingProjects\IDEAProjects"
target_path = os.path.join(base_target_path, "zzz_scripts_" + datetime.now().strftime("%Y%m%d"))

with zipfile.ZipFile(file_path) as zif_obj:
    zif_obj.extractall(path=target_path)

