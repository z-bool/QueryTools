from parsel import Selector
import requests
import random
import time

from mode.singleton import Singleton
from util.UsA import User_Agent_Pool
from log.outputlog import Log


@Singleton
class Requests:
    def __init__(self):
        self.__init()

    def client(
            self,
            url,
            method="get",
            head=None,
            data=None,
            params=None,
            proxy=None,
            retry_time=3,
            retry_interval=5,
            timeout=5,
            *args,
            **kwargs
    ):
        """
        :param url: 请求URL
        :param method: 请求方式：默认GET
        :param head: headers
        :param data: POST请求参数(formdata)
        :param params: GET请求参数
        :param proxy: 代理
        :param retry_time:
        :param retry_interval:
        :param timeout: 请求超时时间
        :param args: 其他
        :param kwargs: 其他
        :return:
        """
        headers = self.headers
        if head and isinstance(head, dict):
            headers.update(head)
        while True:
            try:
                if method == "get" or method.upper() == "GET":
                    self.response = requests.get(
                        url,
                        headers=headers,
                        timeout=timeout,
                        proxies=proxy,
                        params=params,
                        *args,
                        **kwargs
                    )
                else:
                    self.response = requests.post(
                        url,
                        headers=headers,
                        timeout=timeout,
                        proxies=proxy,
                        data=data,
                    )
                if self.response.status_code != 200:
                    self.response.raise_for_status()
                return self
            except (
                    Exception,
                    requests.RequestException
            ):
                Log.error("Request Error:")
                retry_time -= 1
                if retry_time <= 0:
                    resp = self.response
                    resp.status_code = 200
                    return self
                time.sleep(retry_interval)

    @property
    def SelectorText(self):
        return Selector(self.response.text)

    @property
    def text(self):
        return self.response.text

    @property
    def json(self):
        try:
            return self.response.json()
        except Exception as e:
            print("Error:{}".format(e))
            return {}

    @property
    def headers(self):
        return {
            "User-Agent": self.user_agent,
            "Accept": "*/*",
            "Connection": "keep-alive",
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def __init(self):
        # self.user_agent = random.choice([UserAgent().chrome])
        self.user_agent = random.choice(User_Agent_Pool)
        self.response = requests.Response()
