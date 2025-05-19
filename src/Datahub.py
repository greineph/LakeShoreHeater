import time
from datetime import datetime

import pandas as pd

from Channel import Channel
from src import InputData
from src.DataReader import DataReader
from src.LiveGraph import LiveGraph


class Datahub:

    def __init__(self, channels: list[Channel], client=None):
        self.channels = channels
        self.client = client

        columns = ["timestamp", "timedelta"]
        for ch in self.channels:
            columns += [f"{key}_{ch.get_input_channel().value}" for key in ch.get_wanted_reading_keys()]
        self.df = pd.DataFrame(columns=columns)

        self.threads = []

    # creates Threads to continuously read, log and show data until destroyed
    def start_logging(self):
        reader = DataReader(channels=self.channels,
                            client=self.client,
                            sample_rate=InputData.SAMPLE_RATE)
        self.threads.append(reader)
        reader.add_subscriber(self)
        # graph = LiveGraph(datahub=self,
        #                   x_axis="timedelta",
        #                   y_axis=["resistance_1"])
        # self.threads.append(graph)
        # reader.add_subscriber(graph)
        reader.start()
        # graph.run()

        # for i in range(20):
        #     print("---------------------------waiting")
        #     time.sleep(2)
        #     self.threads[1].update(None)

    # writes next free line in self.df with {data}
    def update(self, data):
        self.df.loc[len(self.df)] = data
        print(data)

    # creates a csv file from the current data in self.df to {path} as {name}
    def write_csv(self, name:  str = "out", path: str = "./data"):
        self.df.to_csv(f"{path}/{name}.csv", encoding="utf-8", index=False)

    def get_data(self) -> pd.DataFrame:
        return self.df

