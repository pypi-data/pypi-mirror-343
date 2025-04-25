# -*- coding: utf-8 -*-
# @Time   : 2025/4/20 16:29
from abc import ABCMeta
from typing import Any

import requests
from urllib3.exceptions import InsecureRequestWarning

from scrawlpy.core.scheduler import Scheduler
from scrawlpy.network.request import Request
from scrawlpy.network.seed_item import SeedItem
from scrawlpy.setting import Settings, _SettingsKeyT
from scrawlpy.utils.logger_util import get_bind_logger

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class AbstractSpider(metaclass=ABCMeta):
    project_name = "abstract_project"  # 项目
    spider_name = "abstract_spider"  # spider 接口
    site = "abstract"  # 站点
    Request = Request
    custom_settings: dict[_SettingsKeyT, Any] | None = None

    def __init__(self, scheduler: Scheduler, **kwargs):
        self.scheduler = scheduler
        self.kwargs = kwargs
        self.spider_config = None
        self.logger = get_bind_logger(self.spider_name)
        self.requests = None
        self.is_daemon = False
        self.requests: Request = Request()
        self.settings: Settings = Settings()
        self.update_settings(kwargs.get("settings"))
        self.settings_dict = self.settings.fields_map()

        self.middlewares = []
        self.pipelines = []

        self.logger.debug(self.settings)

    def update_settings(self, cmd_settings):
        """
        获取设置
        Args:
            cmd_settings:

        Returns:

        """

        if not cmd_settings:
            cmd_settings = dict()
        if not self.custom_settings:
            self.custom_settings = dict()
        # 合并自定义设置和命令行设置，命令行设置优先级更高
        combined_settings = {**self.custom_settings, **cmd_settings}

        # 将有效的设置和额外设置传递给Settings类的构造函数
        for k, v in combined_settings.items():
            # 判断是否存在该属性，如果存在则需要根据类型进行转换，否则直接赋值
            if hasattr(self.settings, k):
                setattr(self.settings, k, self.settings.convert_type(self.settings.fields_map_type()[k], v))
            else:
                setattr(self.settings, k, v)

    def add_middleware(self, middleware, priority=0):
        self.middlewares.append((middleware, priority))
        self.middlewares.sort(key=lambda x: x[1])

    def add_pipeline(self, pipeline, priority=0):
        self.pipelines.append((pipeline, priority))
        self.pipelines.sort(key=lambda x: x[1])

    def start_requests(self, seed_item: SeedItem):
        raise NotImplementedError("start_requests method needs to be implemented")

    def parse(self, response):
        raise NotImplementedError("parse method needs to be implemented")

    def parse(self, response, **kwargs):
        pass
