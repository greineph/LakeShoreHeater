import MultiPyVu as mpv
import InputData


class MPVWrapper:

    def __init__(self):
        self.server = mpv.Server()
        self.client = mpv.Client()

        self.wanted_reading_keys = []
        self.wanted_reading_names = []
        self.wanted_plotting_names = []

        self.key_to_function = {"temperature": self.client.get_temperature,
                                "field": self.client.get_field}

        self.server.open()
        self.client.open()

    # TODO: maybe dont open/close client every time, disable logs of mpv somehow
    def get_wanted_readings(self) -> list:
        readings = []
        for key in self.get_wanted_reading_keys():
            readings.append(self.key_to_function[key]()[0])
        return readings

    # gets the selected readings from InputData
    def get_wanted_reading_keys(self) -> list[str]:
        return self.wanted_reading_keys

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
