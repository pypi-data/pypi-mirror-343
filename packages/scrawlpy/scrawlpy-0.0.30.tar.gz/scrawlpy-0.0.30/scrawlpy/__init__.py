# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/20 10:37
@Author  : jayden
"""
import os
import re
import sys

sys.path.insert(0, re.sub(r"([\\/]items$)|([\\/]spiders$)", "", os.getcwd()))

__all__ = [
    "AirSpider",
    "Spider",
    "Request",
    "ArgumentParser",
]

from scrawlpy.core.spiders import AirSpider, Spider
from scrawlpy.network.request import Request
from scrawlpy.utils.custom_argparse import ArgumentParser

from scrawlpy.core.spiders import Spider
from scrawlpy.core.spiders import AirSpider
from scrawlpy.network.request import Request