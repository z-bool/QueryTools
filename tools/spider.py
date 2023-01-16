# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/11 0:00
# @IDE: PyCharm
import json
import random
import re
from collections import defaultdict
from types import SimpleNamespace
from threading import Thread

import requests
import tldextract
from fake_useragent import UserAgent
from parsel import Selector

from tools.func import is_domain, fHideMid


class SpiderTask(Thread):
    def __init__(self):
        super(SpiderTask, self).__init__()
        self.headers = {"user-agent": random.choice([UserAgent().chrome])}
        self.SimpleNamespace = SimpleNamespace
        self.Selector = Selector

    def ip_address(self, ip):
        url = "https://webscan.cc/"
        data = {
            "domain": ip
        }
        response = requests.post(url, headers=self.headers, data=data)
        selector = self.Selector(response.text)
        address = selector.css("body > div > div > div.inner > div.module.mod-intro > div > h2::text").extract_first()
        if address != "The URL you entered does not meet the specification. Please check and try again!":
            return address

    def query_ip_domain(self, ip):
        domainList = defaultdict(list)
        url = f"https://api.webscan.cc/?action=query&ip={ip}"
        resp = requests.get(url, headers=self.headers).text
        if resp != 'null':
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
            return self.SimpleNamespace(domain_lists=list(set(domainList.get("domain_list"))))

    def query_registered_capital(self, sponsor_name):
        url = "https://www.tianyancha.com/search"
        if sponsor_name:
            if len(sponsor_name) == 2 or len(sponsor_name) == 3:
                return None
            params = {
                "key": sponsor_name
            }
            response = requests.get(url, params=params, headers=self.headers).text
            results = re.search('<span title=".*?">(.*?)</span>', response)
            if results is not None:
                return results.group(1).replace("万人民币", "W")

    def query_domain_seo(self, domain):
        self.headers['Referer'] = "https://www.aizhan.com/"
        url = 'https://baidurank.aizhan.com/baidu/{url}'.format(url=domain)
        response = requests.get(url, headers=self.headers).text
        results = re.search(
            '<li><em>权重：</em><img align="absmiddle" alt="权重" src="//statics.aizhan.com/images/br/(.*?).png"/></li>',
            response)
        if results:
            return results.group(1)

    def record_inquiry(self, domain: str) -> SimpleNamespace:
        if is_domain(domain):
            self.headers['referer'] = f"https://www.aiunv.com/icp/{domain}"
            url = f"https://www.aiunv.com/icp/{domain}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                sel = Selector(response.text)
                icp = sel.css("#result > table > tr:nth-child(3) > td:nth-child(2)::text").extract_first()
                mc = sel.css("#result > table > tr:nth-child(4) > td:nth-child(2)::text").extract_first()
                xz = sel.css("#result > table > tr:nth-child(5) > td:nth-child(2)::text").extract_first()
                times = sel.css("#result > table > tr:nth-child(7) > td:nth-child(2)::text").extract_first()
                return self.SimpleNamespace(
                    record={
                        "domain": domain,
                        "sponsor_name": mc,
                        "sponsor_property": xz,
                        "domain_icp": icp,
                        "time": times,
                        "capital": self.query_registered_capital(mc),
                        "seo": self.query_domain_seo(domain)
                    }
                )
