import time
from datetime import datetime

import pandas as pd

from Channel import Channel
from src import InputData
from src.DataReader import DataReader
from src.LiveGraph import LiveGraph
from MPVWrapper import MPVWrapper


class Datahub:

    def __init__(self, channels: list[Channel], mpv_wrapper: MPVWrapper = None):
        self.channels = channels
        self.mpv_wrapper = mpv_wrapper

        columns = ["timestamp", "timedelta"]
        for ch in self.channels:
            columns += ch.wanted_reading_names
        if self.mpv_wrapper:
            columns += mpv_wrapper.wanted_reading_names
        self.df = pd.DataFrame(columns=columns)

        self.reader = None
        self.graph = None

    # creates Threads to continuously read, log and show data until destroyed
    def start_logging(self, logging_interval=5):
        self.reader = DataReader(channels=self.channels,
                                 mpv_wrapper=self.mpv_wrapper,
                                 logging_interval=logging_interval)
        self.reader.daemon = True
        self.reader.add_subscriber(self)

        plotting_names = []
        for ch in self.channels:
            plotting_names += ch.wanted_plotting_names
        plotting_names += self.mpv_wrapper.wanted_plotting_names
        self.graph = LiveGraph(datahub=self,
                               x_axis="timedelta",
                               y_axis=plotting_names)

        self.reader.start()
        self.graph.initialize()

        while True:
            time.sleep(0.1)
            self.graph.update()

    # appends {data} to self.df
    def update(self, data):
        self.df.loc[len(self.df)] = data
        print(data)

    # creates a csv file from the current data in self.df to {path} as {name}
    def write_csv(self, name:  str = "out", path: str = "./data"):
        self.df.to_csv(f"{path}/{name}.csv", encoding="utf-8", index=False)

    def get_data(self) -> pd.DataFrame:
        return self.df

