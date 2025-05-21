import time
from datetime import datetime
import threading
import pandas as pd

from src.Channel import Channel
from src.MPVWrapper import MPVWrapper


class DataReader(threading.Thread):

    def __init__(self, channels: list[Channel], mpv_wrapper: MPVWrapper = None, sample_rate: float = 5):
        super().__init__()
        self.channels = channels
        self.mpv_wrapper = mpv_wrapper
        self.sample_rate = sample_rate
        self.subscribers = []
        self.is_running = False

    def run(self):
        start_timestamp = datetime.now()

        self.is_running = True
        while self.is_running:
            row = [datetime.now().time(), (datetime.now() - start_timestamp).total_seconds()]
            for ch in self.channels:
                row += ch.get_wanted_readings()
            if self.mpv_wrapper:
                row += self.mpv_wrapper.get_wanted_readings()
            self.notify_subscribers(data=row)
            time.sleep(self.sample_rate)

    # Observer-pattern:
    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)
