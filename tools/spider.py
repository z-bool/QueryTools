# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/11 0:00
# @IDE: PyCharm
import json
import re
from collections import defaultdict
from types import SimpleNamespace
import random
import requests
import tldextract
from fake_useragent import UserAgent
from parsel import Selector
from tools.func import is_domain, get_alexa_token, time_sleep


class SpiderTask:
    def __init__(self):
        super(SpiderTask, self).__init__()
        self.__init()

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
                # return results.group(1).replace("万人民币", "W")
                return results.group(1)

    def query_domain_seo(self, domain):
        self.headers['Referer'] = "https://www.aizhan.com/"
        url = 'https://baidurank.aizhan.com/baidu/{url}'.format(url=domain)
        response = requests.get(url, headers=self.headers).text
        results = re.search(
            '<li><em>权重：</em><img align="absmiddle" alt="权重" src="//statics.aizhan.com/images/br/(.*?).png"/></li>',
            response)
        if results:
            return results.group(1)

    def record_inquiry(self, domain: str):
        global mc, xz, icp
        if is_domain(domain):
            while True:
                url = self.icp_url.format(domain)
                response = requests.get(url, headers=self.headers)
                try:
                    if response.status_code != 200:
                        response.raise_for_status()
                    if "icplishi" in url:
                        selector = Selector(response.text)
                        for sel in selector.css("body > div > div.container > div > div.module.mod-panel > div.bd > "
                                                "div:nth-child(1) > div.c-bd > table > tbody"):
                            xz = sel.css("tr:nth-child(2) > td:nth-child(2) > span::text").extract_first()
                            mc = sel.css("tr:nth-child(3) > td:nth-child(2) > a::text").extract_first()
                            icp = sel.css("tr:nth-child(4) > td:nth-child(2) > a::text").extract_first()

                    if "alexa" in url:
                        token = self.__alexa_token(response.text)
                        data = self.__get_token(token, domain)
                        mc = data.get("data", '').get("com_name", '')
                        xz = data.get("data").get("icp_type")
                        icp = data.get("data").get("icp_no")

                    if "api" in url:
                        icp = response.json().get("icp")
                        mc = response.json().get("name")
                        xz = response.json().get("tyle")

                    return self.SimpleNamespace(
                        record={
                            "domain": domain,
                            "sponsor_name": mc,
                            "sponsor_property": xz,
                            "domain_icp": icp,
                            # "time": times,
                            "capital": self.query_registered_capital(mc),
                            "seo": self.query_domain_seo(domain)
                        }
                    )

                except requests.RequestException:
                    print("状态码: {}异常,尝试切换线路中....".format(response.status_code))
                    break

    def __get_token(self, token, domain):
        resp = requests.get(self.alexa_url.format(token=token, domain=domain), headers=self.headers)
        if resp.status_code == 200:
            if len(resp.json()) == 3:
                return resp.json()

    def __alexa_token(self, response):
        com = re.compile("ICP_home_load\\('#ICP',((?:.|\n)*?)\\)")
        resp = re.findall(com, response)
        if len(resp):
            resp = resp[0].replace("{", '').replace("}", '').strip()
            comm = re.compile("token : '(.*?)',")
            token = re.findall(comm, resp)
            return token[0]

    def __init(self):
        self.headers = {"user-agent": random.choice([UserAgent().chrome])}
        self.SimpleNamespace = SimpleNamespace
        self.Selector = Selector
        self.alexa_url = "http://www.alexa.cn/api/icp/info?token={token}&url={domain}&host=&vcode="
        self.icp_url = random.choice([
            "http://www.alexa.cn/{}",
            "https://icplishi.com/{}/",
            "https://v.api.aa1.cn/api/icp/index.php?url={}"
        ])


class SpiderCollectionRecord:
    def __init__(self) -> None:
        self.__init()

    def get_record(self, domain: str = None):
        global url, resp
        mc = None
        xz = None
        icp = None
        if is_domain(domain=domain):
            while True:
                try:
                    url = random.choice(self.icp_url).format(domain)
                    resp = requests.get(url=url, headers=self.headers, allow_redirects=False)
                    time_sleep()
                    if resp.status_code in [503, 502, 404, 302, 403]:
                        resp.raise_for_status()
                    if "alexa" in url:
                        # print("线路：1")
                        time_sleep()
                        response = self.__get_alexa(html=resp.text, domain=domain)
                        r = response.json()
                        if r.get("status") != 102 and r.get("data") != []:
                            r = r.get("data")
                            mc = r.get("com_name")
                            icp = r.get("icp_no_main")
                            xz = r.get("icp_type")

                    elif "icplishi" in url:
                        # print("线路：2")
                        time_sleep()
                        selector = Selector(resp.text)
                        for sel in selector.css(
                                "body > div > div.container > div > div.module.mod-panel > div.bd > "
                                "div:nth-child(1) > div.c-bd > table > tbody"):
                            xz = sel.css("tr:nth-child(2) > td:nth-child(2) > span::text").extract_first()
                            mc = sel.css("tr:nth-child(3) > td:nth-child(2) > a::text").extract_first()
                            icp = sel.css("tr:nth-child(4) > td:nth-child(2) > a::text").extract_first()
                            if [xz, mc, icp] is not None:
                                xz = xz.strip()
                                mc = mc.strip()
                                icp = icp.strip()

                    elif "v.api.aa1" in url:
                        # print("线路：3")
                        time_sleep()
                        r = resp.json()
                        if r.get("name") != "null" or r.get("icp") != "服务器请求频率过高，请稍后再试":
                            icp = r.get("icp")
                            mc = r.get("name")
                            xz = r.get("type")
                    elif "icp.chinaz.com" in url:
                        # print("线路：4")
                        time_sleep()
                        selector = Selector(resp.text)
                        for sel in selector.css("#first"):
                            xz = sel.css(
                                "li:nth-child(2) > p > strong::text").extract_first()
                            mc = sel.css(
                                "li:nth-child(1) > p > a::text").extract_first()
                            icp = sel.css(
                                "li:nth-child(3) p font::text").extract_first()

                    elif "beianx.cn" in url:
                        # print("线路：5")
                        time_sleep()
                        selector = Selector(resp.text)
                        for sel in selector.css("body > div:nth-child(4) > table > tbody > tr"):
                            mc = sel.css("td:nth-child(2) > a::text").extract_first()
                            xz = sel.css("td:nth-child(3)::text").extract_first()
                            icp = sel.css("td:nth-child(4)::text").extract_first()
                            if mc is not None:
                                mc = mc.strip()
                            if xz is not None:
                                xz = xz.strip()
                            if icp is not None:
                                icp = icp.strip()

                    return self.SimpleNamespace(
                        record={
                            "domain": domain,
                            "sponsor_name": mc,
                            "sponsor_property": xz,
                            "domain_icp": icp,
                        }
                    )
                except requests.RequestException:
                    print("当前icp线路异常,尝试切换线路中.........")
                    time_sleep()
                    continue

    def __get_alexa(self, html, domain):
        token = get_alexa_token(html)
        resp = requests.get(self.alexa_url.format(token=token, domain=domain))
        return resp

    def __init(self):
        self.SimpleNamespace = SimpleNamespace
        self.headers = {"user-agent": random.choice([UserAgent().chrome])}
        self.alexa_url = "http://www.alexa.cn/api/icp/info?token={token}&url={domain}&host=&vcode="
        self.icplishi_url = "https://icplishi.com/query.do?domain={domain}&token={token}&time={times}"
        self.icp_url = [
            "http://www.alexa.cn/{}",
            "https://icplishi.com/{}/",
            "https://v.api.aa1.cn/api/icp/index.php?url={}",
            "https://icp.chinaz.com/{}",
            "https://www.beianx.cn/search/{}",
        ]


# print(SpiderCollectionRecord().get_record("dhpin.com"))