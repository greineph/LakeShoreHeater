import time
from datetime import datetime
import threading
from enum import Enum

import pandas as pd

from src.Channel import Channel
from src.MPVWrapper import MPVWrapper


class DataReader(threading.Thread):

    def __init__(self, channels: list[Channel], mpv_wrapper: MPVWrapper = None, logging_interval: float = 5,
                 instruction_queue=None):
        super().__init__()
        if instruction_queue is None:
            instruction_queue = []
        self.channels = channels
        self.mpv_wrapper = mpv_wrapper
        self.logging_interval = logging_interval
        self.subscribers = []
        self.is_running = False
        self.is_reading = False
        self.instruction_queue = instruction_queue

    def run(self):
        start_timestamp = datetime.now()
        start_time = time.monotonic()

        self.is_running = True
        self.is_reading = True
        while self.is_running:
            for instruction in self.instruction_queue:
                self.execute_instruction(instruction)
                self.instruction_queue.remove(instruction)
            if self.is_reading:
                row = [datetime.now(), (datetime.now() - start_timestamp).total_seconds()]
                for ch in self.channels:
                    row += ch.get_wanted_readings()
                if self.mpv_wrapper:
                    row += self.mpv_wrapper.get_wanted_readings()
                self.notify_subscribers(data=row)

            time.sleep(self.logging_interval - ((time.monotonic() - start_time) % self.logging_interval))

    # Observer-pattern:
    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def remove_subscriber(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, data):
        for subscriber in self.subscribers:
            subscriber.update(data)

    def pause(self):
        self.is_reading = False

    def unpause(self):
        self.is_reading = True

    # stops the reader
    def stop(self):
        self.is_running = False

    def execute_instruction(self, instruction):
        match instruction:
            case Instructions.PAUSE:
                self.pause()
            case Instructions.UNPAUSE:
                self.unpause()
            case _:
                pass


class Instructions(Enum):
    PAUSE = 0
    UNPAUSE = 1
