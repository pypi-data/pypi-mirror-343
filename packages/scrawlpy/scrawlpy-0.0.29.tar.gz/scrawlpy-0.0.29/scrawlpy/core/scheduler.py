import json
import time

from scrawlpy.network.seed_item import SeedItem
from scrawlpy.storage.memorydb import PriorityQueue
import redis


class Scheduler:
    def __init__(self, settings, seed_source='file', seed_path=None):
        self.settings = settings
        self.queue = PriorityQueue()

        self.seed_source = seed_source
        self.seed_path = seed_path
        # self.redis_conn = redis.Redis(
        #     host=self.settings.REDIS_HOST,
        #     port=self.settings.REDIS_PORT,
        #     db=self.settings.REDIS_DB
        # )

    def start_task_distribute(self, shutdown_event) -> None:
        """
        分发任务
        Returns:

        """
        n = 0
        while not shutdown_event.is_set():
            # self.queue.put({"url": "https://www.baidu.com"}, )
            # self.queue.put({"url": "https://www.qq.com"}, )
            self.queue.put("https://www.baidu.com", 1)
            self.queue.put("https://www.baidu.com", 1)
            n += 2
            print('当前任务数: {}'.format(n))
            time.sleep(0.1)
        # self.logger.info(f"到超时时间了，任务分发结束...")

    def load_seeds(self, shutdown_event):
        if self.seed_source == 'file3':
            with open(self.seed_path, 'r') as f:
                for line in f:
                    seed_data = json.loads(line.strip())
                    seed = seed_data.get("seed")
                    sys_meta = seed_data.get("sys_meta", {})
                    # request = Request(seed=seed, meta={"sys_meta": sys_meta})
                    seed_item = SeedItem(seed=seed, meta={"sys_meta": sys_meta})
                    self.queue.put(seed_item)
            shutdown_event.set()
        elif self.seed_source == 'redis':
            while not shutdown_event.is_set():
                seed_data = self.redis_conn.lpop(self.settings.TAB_REQUESTS.format(redis_key=self.seed_path))
                if seed_data:
                    seed_json = json.loads(seed_data.decode())
                    seed = seed_json.get("seed")
                    sys_meta = seed_json.get("sys_meta", {})
                    seed_item = SeedItem(seed=seed, meta={"sys_meta": sys_meta})
                    self.queue.put(seed_item)
                else:
                    time.sleep(1)
        else:
            self.start_task_distribute(shutdown_event)

    def add_seed(self, seed: any, priority: int = 0) -> None:
        """
        添加数据到优先级队列中
        Args:
            seed: 数据
            priority: 优先级，数字越小优先级越高
        """
        self.queue.put(seed, priority)

    def get_request(self):
        try:
            return self.queue.get(timeout=1)
        except self.queue.is_empty():
            return None
