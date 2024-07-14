import os.path
import csv
import time
from os.path import basename, dirname


class ZipFileCodec:
    _codec_types = {2: bin, 8: oct, 16: hex, 10: int}

    def __init__(self, pers_path="tmp_pers_path", codec_type=10):
        self.data = []
        self.pers_path = os.path.splitext(pers_path)[0] + ".csv"
        self.codec_type = codec_type

    def _check_codec_type(self):
        if not self.codec_type in self._codec_types:
            raise Exception(f"codec_type({self.codec_type}) 必须在 {self._codec_types.keys()} 范围内")

    def _persistence(self):
        with open(self.pers_path, "w", newline="") as fw:
            csv_writer = csv.writer(fw)
            csv_writer.writerow(self.data)
        self.data = []

    @classmethod
    def _check_zip_extension(cls, filepath: str):
        if not filepath.endswith(".zip"):
            raise Exception(f"{basename(filepath)} 的后缀必须是 .zip")

    def _encode_by_codec_type(self, val):
        if self.codec_type == 10:
            return str(val)
        return self._codec_types[self.codec_type](val)[2:]

    def encode(self, zip_file):
        self._check_zip_extension(zip_file)
        print(f"开始序列化 {basename(zip_file)} 文件")
        time_s = time.time()

        with open(zip_file, "rb") as file:
            with open(self.pers_path, "w", newline="") as fw:
                csv_writer = csv.writer(fw)
                # file.read() 迭代出来的就是 int，写入的时候会被转为字符串
                csv_writer.writerow(self._encode_by_codec_type(e) for e in file.read())

        print(f"序列化 {basename(zip_file)} 到 {basename(self.pers_path)} 文件中成功，"
              f"文件大小：{os.path.getsize(self.pers_path) / 1024 / 1024:.6f} MB，"
              f"耗时：{time.time() - time_s:.2f} s")

    def _decode_by_codec_type(self, val):
        return int(val, self.codec_type)

    def decode(self, zip_file):
        if not os.path.exists(self.pers_path):
            raise Exception("必须在 encode 函数之后执行该函数！")
        self._check_zip_extension(zip_file)

        print(f"开始反序列化 {basename(self.pers_path)} 文件")
        time_s = time.time()

        size = 0
        with open(self.pers_path, "r", newline="") as fr:
            csv_reader = csv.reader(fr)
            with open(zip_file, "wb") as fwb:
                for row in csv_reader:
                    for val in row:
                        size += 1
                        fwb.write(int.to_bytes(self._decode_by_codec_type(val), length=1, byteorder="big"))

        print(f"反序列化 {basename(self.pers_path)} 到 {basename(zip_file)} 文件中成功，"
              f"文件大小：{size / 1024 / 1024:.6f} MB，"
              f"耗时：{time.time() - time_s:.2f} s")

    @staticmethod
    def test():
        zip_file_codec = ZipFileCodec("zip_test_out_binary")
        # zip_file_codec.encode(r"D:\games\Steam\steamapps\common\Don't Starve Together\data\databundles\scripts.zip")
        zip_file_codec.encode(r"markdowns.zip")
        zip_file_codec.decode("zip_test_out.zip")


if __name__ == '__main__':
    zfc = ZipFileCodec("PyQt5Project_240628_1.csv",16)
    zfc.encode(r"C:\Users\zWX1333091\Desktop\PyQt5Project.zip")
    zfc.decode(r"PyQt5Project_2.zip")
