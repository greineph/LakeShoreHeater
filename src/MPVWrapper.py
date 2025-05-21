import MultiPyVu as mpv
import InputData


class MPVWrapper:

    def __init__(self, path_for_settings=""):
        self.server = mpv.Server()
        self.client = mpv.Client()

        self.configure_settings(path_for_settings)

        self.server.open()

        self.key_to_function = {"temperature": self.client.get_temperature,
                                "field": self.client.get_field}

    # TODO: get and set settings
    def configure_settings(self, path) -> None:
        pass

    def get_wanted_readings(self) -> list:
        readings = []
        self.client.open()
        for key in self.get_wanted_reading_keys():
            readings.append(self.key_to_function[key]()[0])
        self.client.close_client()
        return readings

    # gets the selected readings from InputData
    def get_wanted_reading_keys(self) -> list[str]:
        return InputData.WANTED_READINGS_MPV

    # handles shutting down the properties in this wrapper
    def shutdown(self):
        self.server.close()

