# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/11 3:15
# @IDE: PyCharm
import json
import random
import re
import time
from functools import wraps
from urllib.parse import quote
import os

import tldextract
from loguru import logger


def log_info(a):
    logger.info(a)


def log_warning(b):
    logger.warning(b)


def str_quote(s):
    return quote(s)


def is_domain(domain) -> bool:
    """
    True = domain
    False = ip
    :param domain:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    if pattern.match(domain):
        return True
    else:
        return False


is_domain("")


def is_ip(ip) -> bool:
    """
    ip = True
    domain = False
    :param ip:
    :return:
    """
    regular = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if regular.match(ip):
        return True


paths = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def open_file_read(file):
    lines = []
    if file:
        with open(
                os.path.join(paths, file),
                'r',
                encoding="utf-8"
        ) as f:
            results = f.readlines()
            for result in results:
                if result.strip():
                    tld = tldextract.extract(result.strip())
                    if tld.subdomain.strip() and tld.suffix.strip(): lines.append(f'{tld.domain}.{tld.suffix}')
                    if tld.subdomain.strip() == '' and tld.suffix.strip() == '':
                        ip = f'{tld.domain}'
                        if is_ip(ip): lines.append(ip)
                    if tld.domain and tld.suffix:
                        domain = f"{tld.domain}.{tld.suffix}"
                        if is_domain(domain): lines.append(domain)
            set_res = list(set(lines))
            return set_res


def open_file_json(data):
    with open("data.json", 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.write(",\n")


def get_alexa_token(html):
    com = re.compile("ICP_home_load\\('#ICP',((?:.|\n)*?)\\)")
    resp = re.findall(com, html)
    if len(resp):
        resp = resp[0].replace("{", '').replace("}", '').strip()
        comm = re.compile("token : '(.*?)',")
        token = re.findall(comm, resp)
        return token[0]


def time_sleep(start: int = 1, end: int = 10):
    time.sleep(random.randint(start, end))


def fHideMid(str, count=6, fix='*'):
    if not str: return ''
    count = int(count)
    str_len = len(str)
    ret_str = ''
    if str_len == 1:
        return str
    elif str_len == 2:
        ret_str = str[0] + '*'
    elif count == 1:
        mid_pos = int(str_len / 2)
        ret_str = str[:mid_pos] + fix + str[mid_pos + 1:]
    else:
        if str_len - 2 > count:
            if count % 2 == 0:
                if str_len % 2 == 0:
                    ret_str = str[:int(str_len / 2 - count / 2)] + count * fix + str[int(str_len / 2 + count / 2):]
                else:
                    ret_str = str[:int((str_len + 1) / 2 - count / 2)] + count * fix + str[int((
                                                                                                       str_len + 1) / 2 + count / 2):]
            else:
                if str_len % 2 == 0:
                    ret_str = str[:int(str_len / 2 - (count - 1) / 2)] + count * fix + str[int(str_len / 2 + (
                            count + 1) / 2):]
                else:
                    ret_str = str[:int((str_len + 1) / 2 - (count + 1) / 2)] + count * fix + str[
                                                                                             int((str_len + 1) / 2 + (
                                                                                                     count - 1) / 2):]
        else:
            ret_str = str[0] + fix * (str_len - 2) + str[-1]

    return ret_str
