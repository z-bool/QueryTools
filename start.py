# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/12 3:32
# @IDE: PyCharm

import argparse

from tools.task import thread_run
from tools.win import window


@window
def cmd_input():
    parser = argparse.ArgumentParser(description="Demo of argparse")
    # python query.py -f text.txt
    # python query.py -f D:\QueryIpTools\text.txt
    parser.add_argument("-f", "--file", default="text.txt")
    args = parser.parse_args()
    file = args.file
    try:
        if file.endswith(".txt"):
            thread_run(file)
        else:
            print("不是一个txt文件噢")
    except:
        print("你的某个步骤错了...")


cmd_input()
