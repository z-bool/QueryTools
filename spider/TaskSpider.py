# # -*- coding: utf-8 -*-
# # @Author  : iceberg
# # @Time    : 2023/1/24 3:25
# # @IDE: PyCharm
# from collections import defaultdict
# from urllib.parse import quote
# import tldextract
# import json
# import re
#
# from QueryTools.mode.singleton import Singleton
# from QueryTools.util.WebRequest import Requests
#
# from QueryTools.spider.Error import tryme
# from QueryTools.conf import ADDRESS
#
#
# # p = GetProxy().proxy
#
# class RecordCollection:
#     @classmethod
#     def run(cls, domain):
#         Count = 3
#         while True:
#             try:
#                 s1 = RecordCollection.record01(domain)
#                 if s1.get("record"):
#                     if s1.get("record")[0] != "服务器请求频率过高，请稍后再试":
#                         return s1
#                 else:
#                     s2 = RecordCollection.record02(domain)
#                     return s2
#
#                 # s3 = RecordCollection.record03(domain)
#                 # return s3
#
#             except Exception:
#                 Count -= 1
#                 if Count == 0:
#                     break
#                 print("尝试重新连接中.....")
#
#     @staticmethod
#     def record01(domain):
#         url = "https://v.api.aa1.cn/api/icp/index.php?url={}".format(domain)
#         resp = Requests().client(url=url, proxy=None).json
#         a = defaultdict(list)
#         if resp != {}:
#             a['record'].append(resp.get("icp"))
#             a['record'].append(resp.get("name"))
#             a['record'].append(resp.get("tyle"))
#         return a
#
#     @staticmethod
#     def record02(domain):
#         url = "http://www.alexa.cn/{}".format(domain)
#         resp = Requests().client(url=url, proxy=None).text
#         token = get_alexa_token(resp)
#         url = "http://www.alexa.cn/api/icp/info?token={token}&url={domain}&host=&vcode=".format(
#             token=token, domain=domain
#         )
#         a = defaultdict(list)
#         resp = Requests().client(url=url).json
#         if resp.get("data"):
#             r = resp.get("data")
#             a['record'].append(r.get("icp_no_main"))
#             a['record'].append(r.get("com_name"))
#             a['record'].append(r.get("icp_type"))
#         return a
#
#     # @staticmethod
#     # def record03(domain):
#     #     url = "https://icplishi.com/{}/".format(domain)
#     #     selector = Requests().client(url=url).SelectorText
#     #     b = defaultdict(list)
#     #     for sel in selector.css("body > div > div.container > div > div.module.mod-panel > div.bd > "
#     #                             "div:nth-child(1) > div.c-bd > table > tbody"):
#     #         b['record'].append(sel.css("tr:nth-child(2) > td:nth-child(2) > span::text").extract_first())
#     #         b['record'].append(sel.css("tr:nth-child(3) > td:nth-child(2) > a::text").extract_first())
#     #         b['record'].append(sel.css("tr:nth-child(4) > td:nth-child(2) > a::text").extract_first())
#     #     return b
#
#
# def get_seo(src):
#     com = re.compile(f"//statics.aizhan.com/images/.*?/(.*?).png")
#     result = re.findall(com, src)
#     return result[0]
#
#
# def get_alexa_token(html):
#     com = re.compile("ICP_home_load\\('#ICP',((?:.|\n)*?)\\)")
#     resp = re.findall(com, html)
#     if len(resp):
#         resp = resp[0].replace("{", '').replace("}", '').strip()
#         comm = re.compile("token : '(.*?)',")
#         token = re.findall(comm, resp)
#         return token[0]
#
#
# @Singleton
# class SpiderTools:
#
#     @staticmethod
#     def spider01(ip):
#         url = "https://webscan.cc/"
#         data = {
#             "domain": ip
#         }
#         a = defaultdict(list)
#         response = Requests().client(url, method="POST", data=data).SelectorText
#         address = response.css("body > div > div > div.inner > div.module.mod-intro > div > h2::text").extract_first()
#         if address != "The URL you entered does not meet the specification. Please check and try again!":
#             a['address'].append(address)
#             return a
#
#     @staticmethod
#     def spider02(ip):
#         domainList = defaultdict(list)
#         url = f"https://api.webscan.cc/?action=query&ip={ip}"
#         resp = Requests().client(url).text
#         if resp != "null":
#             for r in json.loads(resp):
#                 domain = r.get("domain", None)
#                 if domain is not None:
#                     tld = tldextract.extract(domain)
#                     if tld.suffix != '':
#                         domain = f"{tld.domain}.{tld.suffix}"
#                     else:
#                         domain = tld.domain
#                     if domain in domainList:
#                         continue
#                     domainList['domain_list'].append(domain)
#             a = list(set(domainList.get("domain_list")))
#             # return SimpleNamespace(domain_list=list(set(domainList.get("domain_list")))).domain_list
#             return a
#
#     @staticmethod
#     def spider03(sponsor_name):
#         url = "https://www.tianyancha.com/search"
#         if sponsor_name:
#             if len(sponsor_name) == 2 or len(sponsor_name) == 3:
#                 return None
#             params = {
#                 "key": sponsor_name
#             }
#             response = Requests().client(url, params=params).text
#             results = re.search('<span title=".*?">(.*?)</span>', response)
#             if results is not None:
#                 return results.group(1)
#
#     # @staticmethod
#     # def spider04(domain):
#     #     resp = Requests().client(url="https://www.aizhan.com/cha/{domain}/".format(domain=domain), proxy=None,
#     #                              allow_redirects=False)
#     #     Selector = resp.SelectorText
#     #     baidu = Selector.css("#baidurank_br > img::attr(src)").extract_first()
#     #     yidong = Selector.css("#baidurank_mbr > img::attr(src)").extract_first()
#     #     sanliuling = Selector.css(r"#\33 60_pr > img::attr(src)").extract_first()
#     #     shenma = Selector.css("#sm_pr > img::attr(src)").extract_first()
#     #     sougou = Selector.css("#sogou_pr > img::attr(src)").extract_first()
#     #     google = Selector.css("#google_pr > img::attr(src)").extract_first()
#     #
#     #     src = [baidu, yidong, sanliuling, shenma, sougou, google]
#     #
#     #     d = defaultdict(list)
#     #     if None not in src:  # all(src)
#     #         for s in src:
#     #             result = get_seo(s)
#     #             d['seo'].append(result)
#     #         return d
#
#     @staticmethod
#     def spider05(domain):
#         url = "https://baidurank.aizhan.com/baidu/{}/".format(domain)
#         resp = Requests().client(url=url)
#         Selector = resp.SelectorText
#         baidu = Selector.css("body > div.baidurank-wrap > div.baidurank-infos.clearfix > div.fl > div.top.active > "
#                              "div.ip > ul > li:nth-child(2) > img::attr(src)").extract_first()
#         if baidu:
#             result = get_seo(baidu)
#             return result
#
#
# query_tools = SpiderTools()
# query_record = RecordCollection()
#
#
# @tryme.try_
# def domain_record(domain):
#     CONST_RESULT = {}
#     result = query_record.run(domain).get("record")
#     if "未备案" in result:
#         CONST_RESULT['domain'] = domain
#         CONST_RESULT['record'] = result
#         CONST_RESULT['seo'] = query_tools.spider05(domain)
#     else:
#         CONST_RESULT['domain'] = domain
#         CONST_RESULT['record'] = result
#         CONST_RESULT['capital'] = query_tools.spider03(result[1])
#         CONST_RESULT['seo'] = query_tools.spider05(domain)
#     return CONST_RESULT
#
#
# @tryme.try_
# def ip_domain_address_record_seo(ip):
#     address = query_tools.spider01(ip).get("address")
#     if address:
#         result = {
#             "ip": ip,
#             "address": address[0],
#             "domain_list": query_tools.spider02(ip)
#         }
#
#         if result.get("domain_list"):
#             for domain in result.get("domain_list"):
#                 if quote(address[0][0:2]) in ADDRESS:
#                     result['record'] = domain_record(domain)
#                 else:
#                     result['seo'] = query_tools.spider05(domain)
#         return result
#
