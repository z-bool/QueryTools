import os
from urllib.parse import quote
import re

import tldextract

from mode.singleton import Singleton

paths = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@Singleton
class FuncTools:
    @staticmethod
    def is_domain(domain):
        """
        判断是否是域名(domain)
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

    @staticmethod
    def is_ip(ip):
        """
        判断是否是IP
        """
        regular = re.compile(
            '^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if regular.match(ip):
            return True

    @staticmethod
    def decode(s):
        """
        编码
        """
        return quote(s)

    @staticmethod
    def fHideMid(str, count=6, fix="*"):
        """
        脱敏处理
        str = 要脱敏的数据
        count = 脱敏数据的长度
        fix = 进行脱敏的符号
        """
        if not str:
            return ''
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
                        ret_str = str[:int(str_len / 2 - count / 2)] + \
                                  count * fix + str[int(str_len / 2 + count / 2):]
                    else:
                        ret_str = str[:int((str_len + 1) / 2 - count / 2)] + count * fix + str[int((
                                                                                                           str_len + 1) / 2 + count / 2):]
                else:
                    if str_len % 2 == 0:
                        ret_str = str[:int(str_len / 2 - (count - 1) / 2)] + count * fix + str[int(str_len / 2 + (
                                count + 1) / 2):]
                    else:
                        ret_str = str[:int((str_len + 1) / 2 - (count + 1) / 2)] + count * fix + str[
                                                                                                 int((
                                                                                                             str_len + 1) / 2 + (
                                                                                                             count - 1) / 2):]
            else:
                ret_str = str[0] + fix * (str_len - 2) + str[-1]

        return ret_str

    @staticmethod
    def readfile(file):
        """
        文件读取,去重域名
        :param file:
        :return: [domain]
        """
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
                        # if tld.suffix in ["com", "xyz", "top", "wang", 'pub', 'xin', 'net', 'cn']:
                        if tld.subdomain.strip() and tld.suffix.strip():
                            lines.append(f'{tld.domain}.{tld.suffix}')
                        if tld.subdomain.strip() == '' and tld.suffix.strip() == '':
                            ip = f'{tld.domain}'
                            if FuncTools().is_ip(ip):
                                lines.append(ip)
                        if tld.domain and tld.suffix:
                            domain = f"{tld.domain}.{tld.suffix}"
                            if FuncTools().is_domain(domain):
                                lines.append(domain)
                set_res = list(set(lines))
                return set_res

#
# func = FuncTools()
# print(func.is_domain("baidu.com"))
# for i in func.readfile("text.txt"):
#     print(i)
