import functools
import json
import pprint
import time
import traceback

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from ui.weather_ui import Ui_Form


# Q: open 不赋值是不是会自动清理？
#   为什么 ../weather_app_config.json 会提示没有这个文件？
#       当前文件不是在 ui 目录下吗？难不成 import 类似 c 的 include ？
SETTINGS = json.load(open(r"weather_app_config.json",encoding="utf-8"))

def clock(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time_s = time.time()
        res = func(*args, **kwargs)
        print("cost: {:.4f} s".format(time.time() - time_s))
        return res

    return wrapper


# @clock
def get_weather_info(city_id):
    base_url = "http://www.weather.com.cn/data/sk/"
    response = requests.get(base_url + str(city_id) + ".html")
    # print(response.encoding) # ISO-8859-1
    response.encoding = "utf-8"
    if response.status_code != 200:
        raise requests.HTTPError(f"response.status_code({response.status_code}) != 200")
    data = response.json()
    return data["weatherinfo"]


def format_weather_info(data):
    return (f"城市：{data['city']}\n"
            f"温度：{data['temp']} 度\n"
            f"风向：{data['WD']}\n"
            f"风力：{data['WSE']} 级\n"
            f"湿度：{data['SD']}")


CITY_CODE = SETTINGS["city_code"]


class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, main):
        super(WorkerThread, self).__init__()
        self.main = main

    # def __del__(self):
    #     self.wait()

    def run(self):
        msg = self.main() or ""
        self.finished.emit(msg)


class Form(Ui_Form):
    def __init__(self, form):
        self.setupUi(form)

        self.weatherComboBox.addItems(SETTINGS["city_code"].keys())

        """ 2024/06/23
            如果不放在线程中，self.resultText.setText("查询中，请等待...") 这段代码无效
                其实不止这个，应该是只要涉及渲染的都无效，比如 self.queryButton.setEnabled(True) 也无效
                原理不知道，可能是因为主循环中 UI 渲染被占用了？
                但是放到线程中之后，就正常了。
            注意事项：线程中似乎只能读取，不能修改，否则会直接崩溃。
                    信息传递的话通过 pyqtSignal 实例传过来，在对应函数中修改。
        """
        self.thread_for_queryButton = WorkerThread(self.get_weather_msg_for_queryButton)
        self.queryButton.clicked.connect(self.query_weather_for_queryButton)
        self.thread_for_queryButton.finished.connect(self.thread_on_finished_for_queryButton)

        self.clearButton.clicked.connect(self.clear_result_for_clearButton)

    def thread_on_finished_for_queryButton(self, msg):
        self.resultText.setText(msg)
        self.queryButton.setEnabled(True)

    def query_weather_for_queryButton(self):
        self.queryButton.setEnabled(False)
        self.resultText.setText("查询中，请等待...")
        self.thread_for_queryButton.start()

    def get_weather_msg_for_queryButton(self):
        time_s = time.time()
        msg = ""
        try:
            city_code = CITY_CODE[self.weatherComboBox.currentText()]
            msg = format_weather_info(get_weather_info(city_code))
        except:
            msg = "查询失败"
            print(traceback.format_exc())
        finally:
            msg += "\n" + "耗时：{:.4f} s".format(time.time() - time_s)
        return msg

    def clear_result_for_clearButton(self):
        self.resultText.clear()


if __name__ == '__main__':
    data = get_weather_info("101010100")
    # pprint.pprint(data)
    print(format_weather_info(data))
