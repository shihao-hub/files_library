"""
    实现周期性移动鼠标以避免睡眠，键盘按下 Ctrl + C 终止进程
    但是有点丑陋...
"""

import datetime
import random
import time

import pyautogui as auto
import keyboard

random.seed(time.time())

# const
TIME_INTERVAL = 60
left_position, right_position = auto.Point(100, 400), auto.Point(1800, 400)

# mut
count = 0

while True:
    # 这里要注意不要点到关闭窗口等
    auto.click(*left_position)
    # 不用随机了，随机的时候有可能会跑到右上角导致进程终结
    # auto.moveTo(*map(lambda x: x + random.randrange(-20, 20), right_position))
    auto.moveTo(*right_position)

    count += 1
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -> 第 {count} 次点击屏幕或移动鼠标")

    auto.sleep(TIME_INTERVAL)
    # 上一行就是在睡眠，所以很难及时执行到下面这段代码，除非开个线程，在线程中终止整个进程？
    if keyboard.is_pressed("ctrl") and keyboard.is_pressed("c"):
        print("按下了 ctrl + c，进程终止")
        break
