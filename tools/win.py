# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/11 7:43
# @IDE: PyCharm

from colorama import Fore
from time import sleep
from functools import wraps


def window(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(Fore.RED + ">>>>>>>>>>Start")
        sleep(2)
        a = """      
                                        _🎈                           
                     (❌)               | |                    
                      _    ___    ___  | |__     ___   _ __    __ _ 
                     | |  / __|  / _ \ | '_ \   / _ \ | '__|  / _` |
                     | | | (__  |  __/ | |_) | |  __/ | |    | (_| |
                     |_|  \___|  \___| |_.__/   \___| |_|     \__, |
                                                               __/ |
                                                              |___/ 
                      Author: iceberg(👀)
                        """

        b = """
                      QueryTools: 安全工具
                        ( 
                        【重点声明】
                        1.接口对请求频率有限制,查询效率较慢,请耐心等待.
                        2.QueryIpTools工具仅用于技术交流学习,请勿用于违法用途,否则与本人无关.
                        3.QueryIpTools工具仅用于技术交流学习,不得用于商业用途,仅做交流学习,仅作技术交流学习.
                        )
                      """
        print(Fore.MAGENTA + a, Fore.RED + b)
        sleep(2)

        result = func(*args, **kwargs)
        return result
    return wrapper
