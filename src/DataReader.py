import time
from datetime import datetime
from multiprocessing import Process
import pandas as pd

from src.Channel import Channel


# TODO: Thread is fine unless performance issues become a thing
class DataReader(Process):

    def __init__(self, channels: list[Channel], client=None, sample_rate: float = 5):
        super().__init__()
        self.channels = channels
        self.client = client
        self.sample_rate = sample_rate
        self.subscribers = []

    # TODO: determine how data is supposed to be read in regards to sample_rate
    def run(self):
        start_timestamp = datetime.now()

        while True:
            row = [datetime.now().time(), (datetime.now() - start_timestamp).total_seconds()]
            for ch in self.channels:
                row += ch.get_wanted_readings()
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
