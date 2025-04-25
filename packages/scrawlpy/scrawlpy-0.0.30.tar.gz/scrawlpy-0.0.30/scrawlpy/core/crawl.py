# -*- coding: utf-8 -*-            
# @Time : 2025/4/25 11:54
import threading
import time

from scrawlpy.core.metrics import Metrics
from scrawlpy.core.scheduler import Scheduler
from scrawlpy.setting import Settings
from scrawlpy.core.spiders.base_spider import AbstractSpider

class Crawler:
    def __init__(self, spider_class, settings=None, **kwargs):
        self.settings = settings or Settings()
        self.scheduler = Scheduler(self.settings, seed_source='file', seed_path=None)
        self.spider:AbstractSpider = spider_class(scheduler=self.scheduler, settings=settings, **kwargs)
        self.middlewares = self.spider.middlewares
        self.pipelines = self.spider.pipelines
        self.shutdown_event = threading.Event()
        self.distribute_shutdown_event = threading.Event()
        self.metrics = Metrics(self.settings)

    def crawl(self, request):
        metrics = Metrics(self.settings)
        try:
            for middleware, _ in self.middlewares:
                request = middleware.pre_process(request)

            response = self.spider.start_requests(request)

            if response:
                for middleware, _ in self.middlewares:
                    response = middleware.after_process(response)
                # metrics.record_seed_status(request.seed, "success")
                # metrics.complete()
                # print(f"Request completed in {metrics.execution_time()} seconds")
                item = self.spider.parse(response)
                for pipeline, _ in self.pipelines:
                    pipeline.process_item(item, self.spider)
                return item
            else:
                metrics.record_seed_status(request.url, "failure")
        except Exception as e:
            for middleware, _ in self.middlewares:
                middleware.except_process(e)
            metrics.record_seed_status(request.url, "failure")
            return None

    def start(self, runtime_limit):
        seed_thread = threading.Thread(target=self.scheduler.load_seeds, args=(self.shutdown_event,))
        seed_thread.start()

        threads = []
        for _ in range(5):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        start_time = time.time()
        while time.time() - start_time < runtime_limit:
            if self.distribute_shutdown_event.is_set() or self.shutdown_event.is_set():
                break
            time.sleep(1)

        self.shutdown_event.set()
        self.spider.logger.info("爬虫已停止, 准备等待5s")
        time.sleep(5)
        self.spider.logger.info("爬虫已停止")
        self.distribute_shutdown_event.set()

        for t in threads:
            t.join()

    def worker(self):
        while not self.distribute_shutdown_event.is_set():
            request = self.scheduler.get_request()
            if request:
                self.crawl(request)
            elif self.shutdown_event.is_set():
                break
            else:
                time.sleep(0.1)


class CrawlerProcess:
    def __init__(self, settings=None):
        self.settings = settings or dict()
        self.crawlers = []

    def crawl(self, spider_class, **kwargs):
        crawler = Crawler(spider_class, settings=self.settings, **kwargs)
        self.crawlers.append(crawler)

    def start(self, runtime_limit):
        for crawler in self.crawlers:
            crawler.start(runtime_limit)