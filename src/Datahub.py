# TODO: everything .u.
import time
from datetime import datetime

import pandas as pd

from Channel import Channel


class Datahub:

    def __init__(self, channels: list[Channel]):
        self.data = None
        self.channels = channels


    # TODO: actually do this in a thread somewhere else
    def log_data(self, amount: int, wait_time: float):
        start_timestamp = datetime.now()
        columns = ["timestamp", "timedelta"]
        for ch in self.channels:
            columns += [f"{key}_{ch.get_input_channel().value}" for key in ch.get_wanted_reading_keys()]

        df = pd.DataFrame(columns=columns)
        print(df)
        for i in range(amount):
            row = [datetime.now().time(), (datetime.now() - start_timestamp).total_seconds()]
            for ch in self.channels:
                row += ch.get_wanted_readings()
            df.loc[i] = row
            print(row)
            time.sleep(wait_time)

        pd.set_option("display.max_columns", 20)
        print(df)
        df.to_csv("./data/out.csv", encoding="utf-8", index=False)