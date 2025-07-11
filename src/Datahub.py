import os
import time
from datetime import datetime
from multiprocessing import Queue

import pandas as pd

from Channel import Channel
from src import InputData
from src.DataReader import DataReader, Instructions
from src.LiveGraph import LiveGraph
from MPVWrapper import MPVWrapper


class Datahub:

    def __init__(self, channels: list[Channel], mpv_wrapper: MPVWrapper = None, save_path="", append_to_file=False, controller=None):
        self.channels = channels
        self.mpv_wrapper = mpv_wrapper
        if len(save_path) > 0:
            self.save_path = save_path
        else:
            self.save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "default.csv"))
        self.append_to_file = append_to_file

        columns = ["timestamp", "timedelta"]
        for ch in self.channels:
            columns += ch.wanted_reading_names
        if self.mpv_wrapper:
            columns += mpv_wrapper.wanted_reading_names
        self.df = pd.DataFrame(columns=columns)

        self.reader = None
        self.graph = None
        self.queue = Queue()
        self.instruction_queue = []
        self.controller = controller

    # creates Threads to continuously read, log and show data until destroyed
    def start_logging(self, logging_interval=5):
        self.reader = DataReader(channels=self.channels,
                                 mpv_wrapper=self.mpv_wrapper,
                                 logging_interval=logging_interval,
                                 instruction_queue=self.instruction_queue)
        self.reader.daemon = True
        self.reader.add_subscriber(self)
        for ch in self.channels:
            ch.start_functionality()

        plotting_names = []
        for ch in self.channels:
            plotting_names += ch.wanted_plotting_names
        if self.mpv_wrapper:
            plotting_names += self.mpv_wrapper.wanted_plotting_names
        self.graph = LiveGraph(queue=self.queue,
                               df=self.df,
                               x_axis="timedelta",
                               y_axis=plotting_names)
        if not self.append_to_file:
            self.write_csv(self.save_path)

        print("starting reader")
        self.reader.start()
        print("reader started")
        self.graph.start()
        print("graph started")

    def pause_logging(self):
        self.instruction_queue.append(Instructions.PAUSE)

    def unpause_logging(self):
        self.instruction_queue.append(Instructions.UNPAUSE)

    # appends {data} to self.df
    def update(self, data):
        self.queue.put(data)
        self.df.loc[len(self.df)] = data
        with open(self.save_path, "a") as file:
            file.write(",".join([str(i) for i in data]) + "\n")
        print(data)

    # creates a csv file from the current data in self.df in {path}
    def write_csv(self, path: str = "./data/out.csv"):
        self.df.to_csv(path, encoding="utf-8", index=False)

    def get_data(self) -> pd.DataFrame:
        return self.df

