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
            columns += [f"{key}_{ch.get_input_channel().value}" for key in ch.get_wanted_reading_keys()]
        if self.mpv_wrapper:
            columns += mpv_wrapper.get_wanted_reading_keys()
        self.df = pd.DataFrame(columns=columns)

        self.reader = None
        self.graph = None

    # creates Threads to continuously read, log and show data until destroyed
    def start_logging(self):
        self.reader = DataReader(channels=self.channels,
                                 mpv_wrapper=self.mpv_wrapper,
                                 sample_rate=InputData.SAMPLE_RATE)
        self.reader.daemon = True
        self.reader.add_subscriber(self)
        self.graph = LiveGraph(datahub=self,
                               x_axis="timedelta",
                               y_axis=["temperature", "field"])
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

