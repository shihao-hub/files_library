import os.path
import csv
import shutil
import time
from os.path import basename, dirname


def reserve_code_file(src_dir, dest_dir):
    src_dir = src_dir.rstrip("\\/")
    dest_dir = dest_dir.rstrip("\\/")

    os_path_join = os.path.join

    for dirpath, subdirs, filenames in os.walk(src_dir):
        # os.path.join("c\","\d") 结果会有问题，不是 "c\d" ...
        rel_path = dirpath.replace(src_dir, "").lstrip("\\/")
        if rel_path.startswith((".venv", ".git", ".idea",)):
            continue
        os.mkdir(os_path_join(dest_dir, rel_path))

        for name in filenames:
            if name.endswith((".py", ".txt", ".bat", ".lua", ".html")):
                shutil.copy(str(os_path_join(dirpath, name)),
                            str(os_path_join(dest_dir, rel_path, name)))


reserve_code_file(r"E:\Edtior_Projects\PyCharmProjects\do_exercises",
                  r"E:\Edtior_Projects\PyCharmProjects\do_exercises\filter")


class ZipFileCodec:
    def __init__(self, pers_path):
        self.data = []
        self.pers_path = os.path.splitext(pers_path)[0] + ".csv"

    def _persistence(self):
        with open(self.pers_path, "w", newline="") as fw:
            csv_writer = csv.writer(fw)
            csv_writer.writerow(self.data)
        self.data = []

    @classmethod
    def _check_zip_extension(cls, filepath: str):
        if not filepath.endswith(".zip"):
            raise Exception(f"{basename(filepath)} 的后缀必须是 .zip")

    def encode(self, zip_file):
        print(f"开始序列化 {basename(zip_file)} 文件")
        time_s = time.time()
        self._check_zip_extension(zip_file)

        with open(zip_file, "rb") as file:
            with open(self.pers_path, "w", newline="") as fw:
                csv_writer = csv.writer(fw)
                csv_writer.writerow(e for e in file.read())
        print(f"序列化 {basename(zip_file)} 到 {basename(self.pers_path)} 文件中成功，"
              f"文件大小：{os.path.getsize(self.pers_path) / 1024 / 1024:.6f} MB，"
              f"耗时：{time.time() - time_s:.2f} s")

    def decode(self, zip_file):
        print(f"开始反序列化 {basename(self.pers_path)} 文件")
        time_s = time.time()
        if not os.path.exists(self.pers_path):
            raise Exception("必须在 encode 函数之后执行该函数！")
        self._check_zip_extension(zip_file)

        size = 0
        with open(self.pers_path, "r", newline="") as fr:
            csv_reader = csv.reader(fr)
            with open(zip_file, "wb") as fwb:
                for row in csv_reader:
                    for byte in row:
                        size += 1
                        fwb.write(int.to_bytes(int(byte), length=1, byteorder="big"))
        print(f"反序列化 {basename(self.pers_path)} 到 {basename(zip_file)} 文件中成功，"
              f"文件大小：{size / 1024 / 1024:.6f} MB，"
              f"耗时：{time.time() - time_s:.2f} s")

    @staticmethod
    def test():
        zip_file_codec = ZipFileCodec("zip_test_out_binary")
        # zip_file_codec.encode(r"D:\games\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts.zip")
        zip_file_codec.encode(r"markdowns.zip")
        zip_file_codec.decode("scripts_out.zip")
