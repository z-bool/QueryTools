# -*- coding: utf-8 -*-
# @Author  : iceberg
# @Time    : 2023/1/24 6:02
# @IDE: PyCharm


from typing import Callable, Dict, Any
from collections import defaultdict
from urllib.parse import quote
from threading import Thread
from functools import wraps
from queue import Queue
import tldextract
import json
import csv
import re

from log.outputlog import Log
from mode.singleton import Singleton
from util.WebRequest import Requests
from util.func import FuncTools

l = Log()

ADDRESS = [
    "%E4%B8%AD%E5%9B%BD", "%E5%8C%97%E4%BA%AC", "%E5%A4%A9%E6%B4%A5", "%E6%B2%B3%E5%8C%97", "%E5%B1%B1%E8%A5%BF",
    "%E5%86%85%E8%92%99", "%E8%BE%BD%E5%AE%81", "%E5%90%89%E6%9E%97", "%E9%BB%91%E9%BE%99%E6%B1%9F",
    "%E4%B8%8A%E6%B5%B7", "%E6%B1%9F%E8%8B%8F", "%E6%B5%99%E6%B1%9F", "%E5%AE%89%E5%BE%BD", "%E7%A6%8F%E5%BB%BA",
    "%E6%B1%9F%E8%A5%BF", "%E5%B1%B1%E4%B8%9C", "%E6%B2%B3%E5%8D%97",
    "%E6%B9%96%E5%8C%97", "%E6%B9%96%E5%8D%97", "%E5%B9%BF%E4%B8%9C", "%E6%B5%B7%E5%8D%97", "%E5%B9%BF%E8%A5%BF",
    "%E9%87%8D%E5%BA%86", "%E5%9B%9B%E5%B7%9D", "%E8%B4%B5%E5%B7%9E",
    "%E4%BA%91%E5%8D%97", "%E8%A5%BF%E8%97%8F", "%E9%99%95%E8%A5%BF", "%E7%94%98%E8%82%83", "%E9%9D%92%E6%B5%B7",
    "%E5%AE%81%E5%A4%8F", "%E6%96%B0%E7%96%86", "%E5%8F%B0%E6%B9%BE",
    "%E9%A6%99%E6%B8%AF", "%E6%BE%B3%E9%97%A8"
]


class TryMe:

    def __init__(self):
        self.exception_: Dict[Any, Callable] = {}

    def try_(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler = None
                for c in self.exception_.keys():
                    if isinstance(e, c):
                        handler = c

                if handler is None:
                    raise e
                # 将异常发生的函数和异常对象传入异常处理函数
                return self.exception_[handler](func, e)

        return wrapper

    def except_(self, *exceptions):
        def decorator(f):
            for e in exceptions:
                self.exception_[e] = f
            return f

        return decorator


tryme = TryMe()


@tryme.except_(Exception)
def handle_zero_division_error(func, e):
    l.error("error: {} -{}".format(func.__name__, str(e)))


# p = GetProxy().proxy

class RecordCollection:
    @classmethod
    def run(cls, domain):
        Count = 3
        while True:
            try:
                s1 = RecordCollection.record01(domain)
                if s1.get("record"):
                    if s1.get("record")[0] != "服务器请求频率过高，请稍后再试":
                        return s1
                else:
                    s2 = RecordCollection.record02(domain)
                    return s2

                # s3 = RecordCollection.record03(domain)
                # return s3

            except Exception:
                Count -= 1
                if Count == 0:
                    break
                l.error("尝试重新连接中.....")

    @staticmethod
    def record01(domain):
        url = "https://v.api.aa1.cn/api/icp/index.php?url={}".format(domain)
        resp = Requests().client(url=url, proxy=None).json
        a = defaultdict(list)
        if resp != {}:
            a['record'].append(resp.get("icp"))
            a['record'].append(resp.get("name"))
            a['record'].append(resp.get("tyle"))
        return a

    @staticmethod
    def record02(domain):
        url = "http://www.alexa.cn/{}".format(domain)
        resp = Requests().client(url=url, proxy=None).text
        token = get_alexa_token(resp)
        url = "http://www.alexa.cn/api/icp/info?token={token}&url={domain}&host=&vcode=".format(
            token=token, domain=domain
        )
        a = defaultdict(list)
        resp = Requests().client(url=url).json
        if resp.get("data"):
            r = resp.get("data")
            a['record'].append(r.get("icp_no_main"))
            a['record'].append(r.get("com_name"))
            a['record'].append(r.get("icp_type"))
        return a

    # @staticmethod
    # def record03(domain):
    #     url = "https://icplishi.com/{}/".format(domain)
    #     selector = Requests().client(url=url).SelectorText
    #     b = defaultdict(list)
    #     for sel in selector.css("body > div > div.container > div > div.module.mod-panel > div.bd > "
    #                             "div:nth-child(1) > div.c-bd > table > tbody"):
    #         b['record'].append(sel.css("tr:nth-child(2) > td:nth-child(2) > span::text").extract_first())
    #         b['record'].append(sel.css("tr:nth-child(3) > td:nth-child(2) > a::text").extract_first())
    #         b['record'].append(sel.css("tr:nth-child(4) > td:nth-child(2) > a::text").extract_first())
    #     return b


def get_seo(src):
    com = re.compile(f"//statics.aizhan.com/images/.*?/(.*?).png")
    result = re.findall(com, src)
    return result[0]


def get_alexa_token(html):
    com = re.compile("ICP_home_load\\('#ICP',((?:.|\n)*?)\\)")
    resp = re.findall(com, html)
    if len(resp):
        resp = resp[0].replace("{", '').replace("}", '').strip()
        comm = re.compile("token : '(.*?)',")
        token = re.findall(comm, resp)
        return token[0]


@Singleton
class SpiderTools:

    @staticmethod
    def spider01(ip):
        url = "https://webscan.cc/"
        data = {
            "domain": ip
        }
        a = defaultdict(list)
        response = Requests().client(url, method="POST", data=data).SelectorText
        address = response.css("body > div > div > div.inner > div.module.mod-intro > div > h2::text").extract_first()
        if address != "The URL you entered does not meet the specification. Please check and try again!":
            a['address'].append(address)
            return a

    @staticmethod
    def spider02(ip):
        domainList = defaultdict(list)
        url = f"https://api.webscan.cc/?action=query&ip={ip}"
        resp = Requests().client(url).text
        if resp != "null":
            for r in json.loads(resp):
                domain = r.get("domain", None)
                if domain is not None:
                    tld = tldextract.extract(domain)
                    if tld.suffix != '':
                        domain = f"{tld.domain}.{tld.suffix}"
                    else:
                        domain = tld.domain
                    if domain in domainList:
                        continue
                    domainList['domain_list'].append(domain)
            a = list(set(domainList.get("domain_list")))
            # return SimpleNamespace(domain_list=list(set(domainList.get("domain_list")))).domain_list
            return a

    @staticmethod
    def spider03(sponsor_name):
        url = "https://www.tianyancha.com/search"
        if sponsor_name:
            if len(sponsor_name) == 2 or len(sponsor_name) == 3:
                return None
            params = {
                "key": sponsor_name
            }
            response = Requests().client(url, params=params).text
            results = re.search('<span title=".*?">(.*?)</span>', response)
            if results is not None:
                return results.group(1)

    # @staticmethod
    # def spider04(domain):
    #     resp = Requests().client(url="https://www.aizhan.com/cha/{domain}/".format(domain=domain), proxy=None,
    #                              allow_redirects=False)
    #     Selector = resp.SelectorText
    #     baidu = Selector.css("#baidurank_br > img::attr(src)").extract_first()
    #     yidong = Selector.css("#baidurank_mbr > img::attr(src)").extract_first()
    #     sanliuling = Selector.css(r"#\33 60_pr > img::attr(src)").extract_first()
    #     shenma = Selector.css("#sm_pr > img::attr(src)").extract_first()
    #     sougou = Selector.css("#sogou_pr > img::attr(src)").extract_first()
    #     google = Selector.css("#google_pr > img::attr(src)").extract_first()
    #
    #     src = [baidu, yidong, sanliuling, shenma, sougou, google]
    #
    #     d = defaultdict(list)
    #     if None not in src:  # all(src)
    #         for s in src:
    #             result = get_seo(s)
    #             d['seo'].append(result)
    #         return d

    @staticmethod
    def spider05(domain):
        url = "https://baidurank.aizhan.com/baidu/{}/".format(domain)
        resp = Requests().client(url=url)
        Selector = resp.SelectorText
        baidu = Selector.css("body > div.baidurank-wrap > div.baidurank-infos.clearfix > div.fl > div.top.active > "
                             "div.ip > ul > li:nth-child(2) > img::attr(src)").extract_first()
        if baidu:
            result = get_seo(baidu)
            return result


query_tools = SpiderTools()
query_record = RecordCollection()


@tryme.try_
def domain_record(domain):
    CONST_RESULT = {}
    result = query_record.run(domain).get("record")
    if "未备案" in result:
        CONST_RESULT['domain'] = domain
        CONST_RESULT['record'] = result
        CONST_RESULT['seo'] = query_tools.spider05(domain)
    else:
        CONST_RESULT['domain'] = domain
        CONST_RESULT['record'] = result
        CONST_RESULT['capital'] = query_tools.spider03(result[1])
        CONST_RESULT['seo'] = query_tools.spider05(domain)
    return CONST_RESULT


@tryme.try_
def ip_domain_address_record_seo(ip):
    address = query_tools.spider01(ip).get("address")
    if address:
        result = {
            "ip": ip,
            "address": address[0],
            "domain_list": query_tools.spider02(ip)
        }

        if result.get("domain_list"):
            for domain in result.get("domain_list"):
                if quote(address[0][0:2]) in ADDRESS:
                    result['record'] = domain_record(domain)
                else:
                    result['seo'] = query_tools.spider05(domain)
        return result


class ThreadDomain(Thread):
    def __init__(self, domain_queue: Queue):
        super(ThreadDomain, self).__init__()
        self.domain_queue = domain_queue
        self.setName("Thread-Domain: ")
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            if self.domain_queue.empty():
                break
            domain = self.domain_queue.get()
            a = domain_record(domain)
            l.info(f"{self.getName()} - {a}")
            aaaascv(a)


class ThreadIp(Thread):
    def __init__(self, ip_queue: Queue, ):
        super(ThreadIp, self).__init__()
        self.ip_queue = ip_queue
        self.setName("Thread-IP: ")
        self.setDaemon(True)

    def run(self) -> None:
        while True:
            ip = self.ip_queue.get()
            a = ip_domain_address_record_seo(ip)
            if a:
                l.info(f"{self.getName()} - {a}")
                aaaascv(a)
                if self.ip_queue.empty():
                    break


def aaaascv(data):
    with open('./result.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data.values())


def main(file):
    domain_queue = Queue()
    ip_queue = Queue()
    func = FuncTools()
    for i in FuncTools().readfile(file):
        if func.is_domain(i):
            domain_queue.put(i)
        if func.is_ip(i):
            ip_queue.put(i)

    tasks = [
        ThreadDomain(domain_queue),
        ThreadIp(ip_queue)
    ]
    for task in tasks:
        task.start()
        task.join()

# 你等会 啊 我电脑试试看