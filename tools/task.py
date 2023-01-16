# -*- coding: utf-8 -*-
# @Author  : iceberg 
# @Time    : 2023/1/11 7:45
# @IDE: PyCharm

from queue import Queue
from threading import Thread, Lock

from tools.func import open_file_read, is_domain, log_warning, str_quote, open_file_json, fHideMid
from tools.spider import SpiderTask
from tools.slice import ArraySlice

mutex = Lock()


class A(Thread):
    def __init__(self, queue: Queue, file: str):
        super(A, self).__init__()
        self.queue = queue
        self.file = file
        self.setDaemon(True)

    def run(self) -> None:
        for line in open_file_read(self.file):
            self.queue.put(line)


class B(Thread):
    def __init__(self, queue: Queue):
        super(B, self).__init__()
        self.queue = queue

    def run(self) -> None:
        while True:
            data = self.queue.get()
            if is_domain(data):
                C(data).start()
            else:
                D(data).start()
            self.queue.task_done()
            if self.queue.empty():
                break


class C(Thread):
    def __init__(self, domain):
        super(C, self).__init__()
        self.setName("start thread task domain: ")
        self.domain = domain

    def run(self) -> None:
        # with mutex:
        data = SpiderTask().record_inquiry(self.domain).record
        open_file_json(data)
        log_warning(f"{self.getName()} {data}")


class D(Thread):
    def __init__(self, ip):
        super(D, self).__init__()
        self.ip = ip
        self.setName("start thread task ip: ")

    def run(self) -> None:
        results = {
            "ip": self.ip,
            "address": SpiderTask().ip_address(self.ip),
            "domain_list": SpiderTask().query_ip_domain(self.ip),
        }
        if str_quote(results.get('address')[0:2]) in ArraySlice:
            if results.get("domain_list"):
                for domain in results.get("domain_list").domain_lists:
                        results['records'] = SpiderTask().record_inquiry(domain)
        else:
            if results.get("domain_list"):
                for domain in results.get("domain_list").domain_lists:
                    results['seo'] = SpiderTask().query_domain_seo(domain)
            else:
                results['seo'] = None
        log_warning(f'{self.getName()} {results}')
        open_file_json(str(results))


def thread_run(file: str):
    queue = Queue()
    task = [A(queue, file), B(queue)]
    for i in task:
        i.start()

    for i in task:
        i.join()
