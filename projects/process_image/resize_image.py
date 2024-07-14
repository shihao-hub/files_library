import collections.abc
import os.path
import time

from PIL import Image


# image_obj = Image.open(r"C:\Users\29580\Desktop\preview_2.jpg")
#
# h, w = image_obj.size
# image_obj.resize((256, 256)).save(r"C:\Users\29580\Desktop\preview_2_1.jpg")
# print(Image.open(r"C:\Users\29580\Desktop\preview_2_1.jpg").size)

def resize_image(path, height, width):
    """
    :param path: str
    :param height: int
    :param width: int
    :return: None
    """
    with Image.open(path) as img:
        new_img = img.resize((height, width),Image.LANCZOS)
        dirname = os.path.dirname(path)
        basename: str = os.path.basename(path)
        dot_pos = basename.find(r".")
        new_img.save(
            os.path.join(
                dirname,
                basename[:dot_pos]
                + "_"
                + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
                + basename[dot_pos:]))


resize_image(r"resources/邮箱.png", 40, 40)
