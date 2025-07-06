import traceback

import MultiPyVu as mpv
import numpy as np

import InputData
import threading


# TODO: make thread save
class MPVWrapper:

    def __init__(self):
        self.server = mpv.Server()
        self.client = mpv.Client()
        self.lock = threading.Lock()

        self.wanted_reading_keys = []
        self.wanted_reading_names = []
        self.wanted_plotting_names = []

        self.key_to_function = {"temperature": self.get_temperature,
                                "field": self.get_field}

        self.server.open()
        self.client.open()

    def get_temperature(self):
        self.lock.acquire(blocking=True)
        value = np.nan
        try:
            value = self.client.get_temperature()[0]
        except Exception:
            print(traceback.format_exc())
        self.lock.release()
        return value

    def get_field(self):
        self.lock.acquire(blocking=True)
        value = np.nan
        try:
            value = self.client.get_field()[0]
        except Exception:
            print(traceback.format_exc())
        self.lock.release()
        return value

    def get_wanted_readings(self) -> list:
        readings = []
        for key in self.get_wanted_reading_keys():
            readings.append(self.key_to_function[key]())
        return readings

    # gets the selected readings from InputData
    def get_wanted_reading_keys(self) -> list[str]:
        return self.wanted_reading_keys

    # returns all possible readings as dict
    def get_readings(self):
        readings = {}
        for key in self.key_to_function:
            readings[key] = self.key_to_function[key]()
        return readings

    # handles shutting down the properties in this wrapper
    def shutdown(self):
        self.client.close_client()
        self.server.close()


class MPVSettings:

    def __init__(self, readings):
        self.readings = readings

    def create_mpv_wrapper(self):
        mpv_wrapper = MPVWrapper()
        mpv_wrapper.wanted_reading_keys = [reading["reading"] for reading in self.readings]
        mpv_wrapper.wanted_reading_names = [reading["custom_name"] for reading in self.readings]
        mpv_wrapper.wanted_plotting_names = [reading["custom_name"] for reading in self.readings if reading["plot"]]
        return mpv_wrapper
