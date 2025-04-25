#!/usr/bin/python3
# -*- coding: utf-8 -*-            
"""
@Time : 2025/4/25 15:34
"""

class SeedItem:
    def __init__(self, seed, meta=None):
        self.seed = seed
        self.meta = meta or {}

    def __str__(self):
        return f"Request(url={self.seed}, meta={self.meta})"