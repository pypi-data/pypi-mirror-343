# -*- coding: utf-8 -*-
# @Time   : 2024/4/28 16:36
from scrawlpy.core.scheduler import Scheduler
from scrawlpy.core.spiders.base_spider import AbstractSpider


class Spider(AbstractSpider):
    def __init__(self, scheduler: Scheduler, **kwargs):
        super().__init__(scheduler, **kwargs)

    def run(self):
        pass
