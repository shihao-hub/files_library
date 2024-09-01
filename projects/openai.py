import argparse
import configparser
import datetime
import re
import time
import os
import threading
from types import SimpleNamespace

import requests

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
lock = threading.Lock()


def is_running_in_pycharm():
    # (NOTE)!: os.environ 是个字典，PyCharm 运行程序的时候，其中会存在 PYCHARM_HOSTED 键
    return "PYCHARM_HOSTED" in os.environ


class CalculateTimeIntervalService:
    def __init__(self):
        self.pre = time.time()

    def get(self):
        # 调用时，会计算上次调用的时间点和此时的时间点的差值（第一个时间点为该类初始化的时间点）
        pre = self.pre
        now = time.time()
        self.pre = now
        return now - pre


class LoggingAspect:
    @staticmethod
    def log_before():
        pass


class OpenAiServiceCommonApi:
    def __init__(self, source):
        self.source = source


class OpenAiServiceSendQuestionHelper:
    def __init__(self, source):
        self.source = source

    @staticmethod
    def generate_payload_by(content):
        return {
            "frequency_penalty": 0,
            "max_tokens": 4096,
            "messages": [{"content": content, "role": "user"}],
            "model": "gpt-4o-mini",
            "presence_penalty": 0,
            "stream": True,
            "temperature": 0.6,
            "top_p": 0.99,
        }

    def get_processed_response_data(self, original_data):
        # 当前的见解：可以使用 cookbook 中的正则表达式扫描器
        res = []
        for e in self.source.target_pattern.finditer(original_data):
            res.append(e.group(1))
        # output = "".join(res).replace(r"\n", "\n").replace(r'\"', '"')[:-4]

        # 2024-08-31：这里用的太奇怪了，正则表达式和转义字符 \ 的相爱相杀？
        replaced = {
            r"\\n": "\n",
            r'\\"': '"'
        }
        output = re.sub("|".join(replaced.keys()),
                        lambda x: replaced["\\" + x.group(0)],
                        "".join(res))[:-4]
        return output

    @staticmethod
    def write_data_to_file(output_data, file_path):
        with lock:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(output_data)

    @staticmethod
    def head_print_for_send_question(question):
        print(f"[{datetime.datetime.now()}] 开始问问题：{question.strip()}")

    def trail_print_for_send_question(self, cost):
        print(f"[{datetime.datetime.now()}] 得到回答，共用时：{cost:.4f} s，"
              f"答案已输出到`{self.source.output}`文件中")


class OpenAiService:
    common_const = SimpleNamespace(**dict(
        config_file_path="./openai.ini",  # 配置文件所在路径
        gpt_data_pattern=r"data: \"(.*)\"", # gpt 返回的数据所需要匹配的内容对应的正则表达式模式串
    ))

    def __init__(self, url, output=None):
        config = self.common_const.config_file_path

        self.url = url
        self.config = configparser.ConfigParser()
        self.time_interval = CalculateTimeIntervalService()
        self.target_pattern = re.compile(self.common_const.gpt_data_pattern)
        self.send_question_helper = OpenAiServiceSendQuestionHelper(self)

        self.config.read(config)

        self.output = output if output else self.config["basic_setting"].get("output")

    def send_question(self, question):
        helper = self.send_question_helper

        helper.head_print_for_send_question(question)

        self.time_interval.get()

        # (NOTE)!: Python 已经提供了异步编程库，此处异步实现。这样就能实现转圈的绘制效果了！《流畅的 Python》还是太全面了
        response = requests.post(self.url, json=helper.generate_payload_by(question), headers=self.config["headers"])
        content = response.content.decode("utf-8")
        output = helper.get_processed_response_data(content)
        helper.write_data_to_file(output, self.output)

        helper.trail_print_for_send_question(self.time_interval.get())
        return output

    # send_question -------------------------------------------------------------------------------------------------- #


openai_service = OpenAiService("https://chat.lify.vip/api/chat/openai")


@app.route("/", methods=["GET"])
def index():
    return render_template("openai_index.html")


@app.route("/question", methods=["POST"])
def send_question():
    json_data = request.get_json()
    return jsonify({
        "result": openai_service.send_question(json_data.get("input_data"))
    })


if __name__ == '__main__':
    # openai_server = OpenAiService("https://chat.lify.vip/api/chat/openai")
    # if not is_running_in_pycharm():
    #     parser = argparse.ArgumentParser(description="OpenAi 问答")
    #     parser.add_argument("question", type=str, help="输入你的问题")
    #     args = parser.parse_args()
    #     question = args.question
    # else:
    #     question = """
    #         如何迅速使用 flask 启动一个服务
    #     """
    # openai_server.send_question(question)
    app.run(debug=True)
