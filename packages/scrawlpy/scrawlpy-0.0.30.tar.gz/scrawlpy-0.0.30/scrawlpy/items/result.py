#!/usr/bin/python3
# -*- coding: utf-8 -*-            
"""
@Time : 2025/4/25 16:46
"""

from pydantic import BaseModel


class Result(BaseModel):
    result: dict = dict()
    result_list: list = list()

    is_split_result_list: bool = True

    status_code: int = 200
