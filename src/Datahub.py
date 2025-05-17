import time
from datetime import datetime

import pandas as pd

from Channel import Channel
from src import InputData
from src.DataReader import DataReader


class Datahub:

    def __init__(self, channels: list[Channel], client=None):
        self.channels = channels
        self.client = client

        columns = ["timestamp", "timedelta"]
        for ch in self.channels:
            columns += [f"{key}_{ch.get_input_channel().value}" for key in ch.get_wanted_reading_keys()]
        self.df = pd.DataFrame(columns=columns)

    # starts a Thread to continuously read and log data until destroyed
    def start_logging(self):
        reader = DataReader(channels=self.channels,
                            client=self.client,
                            sample_rate=InputData.SAMPLE_RATE)
        reader.add_subscriber(self)
        # TODO: add live diagram to subscribers
        reader.start()

    # writes next free line in self.df with {data}
    def update(self, data):
        self.df.loc[len(self.df)] = data

    # creates a csv file from the current data in self.df to {path} as {name}
    def write_csv(self, name:  str = "out", path: str = "./data"):
        self.df.to_csv(f"{path}/{name}.csv", encoding="utf-8", index=False)

