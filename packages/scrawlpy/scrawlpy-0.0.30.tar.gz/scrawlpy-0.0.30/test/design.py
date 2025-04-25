import os
import time
import threading
import queue
import requests
import redis
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision


# 基本配置
class BaseSettings:
    Timeout = float(os.environ.get("Timeout", 2))
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    TAB_REQUESTS = "{redis_key}:z_requests"
    TAB_FAILED_REQUESTS = "{redis_key}:z_failed_requests"
    TAB_FAILED_ITEMS = "{redis_key}:s_failed_items"
    TAB_SPIDER_STATUS = "{redis_key}:h_spider_status"
    TAB_USER_POOL = "{redis_key}:h_{user_type}_pool"

    INFLUXDB_URL = "http://localhost:8086"
    INFLUXDB_TOKEN = "your-token"
    INFLUXDB_ORG = "your-org"
    INFLUXDB_BUCKET = "your-bucket"


class Settings(BaseSettings):
    pass


class Request:
    def __init__(self, seed, meta=None):
        self.seed = seed
        self.meta = meta or {}

    def __str__(self):
        return f"Request(url={self.seed}, meta={self.meta})"


class Response:
    def __init__(self, url, status_code, text, meta=None):
        self.url = url
        self.status_code = status_code
        self.text = text
        self.meta = meta or {}

    def __str__(self):
        return f"Response(url={self.url}, status_code={self.status_code})"


class Metrics:
    def __init__(self, settings):
        self.client = InfluxDBClient(
            url=settings.INFLUXDB_URL,
            token=settings.INFLUXDB_TOKEN,
            org=settings.INFLUXDB_ORG
        )
        self.bucket = settings.INFLUXDB_BUCKET
        self.job_id = None
        self.user = None

        self.start_time = time.time()
        self.end_time = None

    def complete(self):
        # Record the completion time and duration
        end_time = time.time()
        self.end_time = time.time()
        duration = end_time - self.start_time
        point = Point("job_metrics").tag("job_id", self.job_id).tag("user", self.user) \
            .field("duration", duration).time(time.time(), WritePrecision.NS)
        self.client.write_api().write(bucket=self.bucket, record=point)

    def record_seed_status(self, seed, status):
        point = Point("seed_metrics").tag("job_id", self.job_id).tag("user", self.user) \
            .tag("seed", seed).field("status", status).time(time.time(), WritePrecision.NS)
        self.client.write_api().write(bucket=self.bucket, record=point)

    def record_output(self, count):
        point = Point("output_metrics").tag("job_id", self.job_id).tag("user", self.user) \
            .field("output_count", count).time(time.time(), WritePrecision.NS)
        self.client.write_api().write(bucket=self.bucket, record=point)

    def execution_time(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None


class Spider:
    name = 'default_spider'

    def __init__(self, settings=None, **kwargs):
        self.settings = settings or Settings()
        self.kwargs = kwargs
        self.middlewares = []
        self.pipelines = []

    def add_middleware(self, middleware, priority=0):
        self.middlewares.append((middleware, priority))
        self.middlewares.sort(key=lambda x: x[1])

    def add_pipeline(self, pipeline, priority=0):
        self.pipelines.append((pipeline, priority))
        self.pipelines.sort(key=lambda x: x[1])

    def start_requests(self, request: Request):
        try:
            url = request.seed.get("url")
            response = requests.get(url, timeout=self.settings.Timeout)
            response.raise_for_status()
            response_obj = Response(
                url=url,
                status_code=response.status_code,
                text=response.text,
                meta=request.meta
            )
            return response_obj
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def parse(self, response):
        raise NotImplementedError("parse method needs to be implemented")


class Middleware:
    def pre_process(self, request):
        return request

    def after_process(self, response):
        return response

    def except_process(self, exception):
        pass


class Pipeline:
    def process_item(self, item, spider):
        # 处理解析后的数据项
        pass


class Scheduler:
    def __init__(self, settings, seed_source='file', seed_path=None):
        self.settings = settings
        self.queue = queue.Queue()
        self.seed_source = seed_source
        self.seed_path = seed_path
        self.redis_conn = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=self.settings.REDIS_DB
        )

    def start_task_distribute(self, shutdown_event) -> None:
        """
        分发任务
        Returns:

        """
        n = 0
        while not shutdown_event.is_set():
            self.queue.put({"url": "https://www.baidu.com"}, )
            self.queue.put({"url": "https://www.qq.com"}, )
            n += 2
            print('当前任务数: {}'.format(n))
            # self.logger.info(f"当前任务数: {n}")
            time.sleep(0.1)
        # self.logger.info(f"到超时时间了，任务分发结束...")

    def load_seeds(self, shutdown_event):
        if self.seed_source == 'file':
            with open(self.seed_path, 'r') as f:
                for line in f:
                    seed_data = json.loads(line.strip())
                    seed = seed_data.get("seed")
                    sys_meta = seed_data.get("sys_meta", {})
                    request = Request(seed=seed, meta={"sys_meta": sys_meta})
                    self.queue.put(request)
            shutdown_event.set()
        elif self.seed_source == 'redis':
            while not shutdown_event.is_set():
                seed_data = self.redis_conn.lpop(self.settings.TAB_REQUESTS.format(redis_key=self.seed_path))
                if seed_data:
                    seed_json = json.loads(seed_data.decode())
                    seed = seed_json.get("seed")
                    sys_meta = seed_json.get("sys_meta", {})
                    request = Request(seed=seed, meta={"sys_meta": sys_meta})
                    self.queue.put(request)
                else:
                    time.sleep(1)
        else:
            self.start_task_distribute(shutdown_event)

    def get_request(self):
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            return None


class Crawler:
    def __init__(self, spider_class, settings=None, **kwargs):
        self.spider = spider_class(settings=settings, **kwargs)
        self.settings = settings or Settings()
        self.scheduler = Scheduler(self.settings, seed_source='file', seed_path=None)
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
                metrics.record_seed_status(request.seed, "success")
                metrics.complete()
                print(f"Request completed in {metrics.execution_time()} seconds")
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

        time.sleep(5)
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
        self.settings = settings or Settings()
        self.crawlers = []

    def crawl(self, spider_class, **kwargs):
        crawler = Crawler(spider_class, settings=self.settings, **kwargs)
        self.crawlers.append(crawler)

    def start(self, runtime_limit):
        for crawler in self.crawlers:
            crawler.start(runtime_limit)


# 示例使用
class ExampleSpider(Spider):
    def start_requests(self, request):
        print(request)

    def parse(self, response):
        # 解析响应
        return response.text


if __name__ == "__main__":
    process = CrawlerProcess(settings=Settings())
    process.crawl(ExampleSpider)
    process.start(runtime_limit=10)  # 设置爬虫运行时间限制，比如10秒
