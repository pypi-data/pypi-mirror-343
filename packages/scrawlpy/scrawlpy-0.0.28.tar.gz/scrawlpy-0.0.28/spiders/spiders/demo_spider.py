# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/20 10:37
@Author  : jayden
"""
import threading
import time

import scrawlpy
from scrawlpy import Spider
from scrawlpy.core.crawl import CrawlerProcess
from scrawlpy.items.result import Result
from scrawlpy.utils.gen_seed import write_seed_json_file

from test.spiders.settings.airspider_settings import SpiderSettings


class Myspider(scrawlpy.AirSpider):
    Settings = SpiderSettings
    __custom_setting__ = {
        "Timeout": "5",
        "KEEP_ALIVE": False,
    }

    def start_task_distribute(self) -> None:
        """
        分发任务
        Returns:

        """
        while True:
            self.request_queue.add({"url": "https://www.baidu.com"}, 1)
            # self.request_queue.add({"url": "https://www.qq.com"}, 2)

    def start_requests(self, seed):
        # print(seed)
        priority, seed = seed
        # self.log.info()
        url = seed.get("url")
        self.logger.info(f"线程id: {threading.get_ident()} 超时时间: {self.settings.Timeout}")
        res = self.requests.get(url)
        # self.logger.info(res.text)
        # for i in range(10):
        #     yield Request("http://www.baidu.com", callback=self.parse)
        # res = self.requests.get("http://www.baidu.com")
        # print(res.text)


# 示例使用
class ExampleSpider(Spider):
    def start_requests(self, request):
        print(request)
        self.scheduler.add_seed("http://www.cip.com", 10)
        size = self.scheduler.queue.size()
        time.sleep(0.4)
        print('size: ', size)
        result = {
            "url": "http://www.baidu.com"
        }
        return Result(result=result, status_code=200)

    # def parse(self, response):
    #     解析响应
    # return response.text


#

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ExampleSpider)
    process.start(runtime_limit=3)  # 设置爬虫运行时间限制，比如10秒
