from Device import Device
from lakeshore import Model372, Model372InputSetupSettings
import InputData


class Channel:

    def __init__(self, device: Model372, input_channel: Model372.InputChannel):
        self.device = device
        self.input_channel = input_channel
        self.configure_setup_settings()
        # self.set_filter()

    # returns readings of {kelvin, resistance, power} as dictionary
    def get_readings(self):
        return self.device.get_all_input_readings(self.input_channel.value)

    # configures channels setup settings in lakeshore device
    def configure_setup_settings(self):
        self.device.configure_input(self.input_channel.value, self.create_input_setup_settings())

    # creates this channels input setup settings from values set in InputData.py
    # @abstract
    def create_input_setup_settings(self) -> Model372InputSetupSettings:
        raise NotImplementedError("Implement this method in subclass")

    # sets the measurement filter for this channel
    def set_filter(self):
        self.device.set_filter(input_channel=self.input_channel.value,
                               state=InputData.STATE_FILTER,
                               settle_time=InputData.SETTLE_TIME_FILTER,
                               window=InputData.WINDOW_FILTER)

    # gets the selected readings from InputData
    # @abstract
    def get_wanted_reading_keys(self) -> list[str]:
        raise NotImplementedError("Implement this method in subclass")

    def get_wanted_readings(self) -> list:
        readings = self.get_readings()
        return [readings[key] for key in self.get_wanted_reading_keys()]

    def get_input_channel(self):
        return self.input_channel
