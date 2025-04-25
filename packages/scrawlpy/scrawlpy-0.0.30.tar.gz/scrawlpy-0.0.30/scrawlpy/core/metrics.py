# -*- coding: utf-8 -*-            
# @Time : 2025/4/25 11:54
import time

from influxdb_client import InfluxDBClient, Point, WritePrecision
from scrawlpy.setting import Settings

class Metrics:
    def __init__(self, settings:Settings):
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
