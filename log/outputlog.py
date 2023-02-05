# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/23 3:30
# @IDE: PyCharm
from loguru import logger


class Log:
    @staticmethod
    def error(data):
        logger.error(data)

    @staticmethod
    def info(data):
        logger.warning(data)
