from bokeh.core.has_props import abstract

from Device import Device
from lakeshore import Model372, Model372InputSetupSettings


class Channel:

    def __init__(self, device: Model372, input_channel: Model372.InputChannel):
        self.device = device
        self.input_channel = input_channel

    # returns readings of {kelvin, resistance, power} as dictionary
    def get_readings(self):
        return self.device.get_all_input_readings(self.input_channel.value)

    # configures channels setup settings in lakeshore device
    def configure_setup_settings(self):
        self.device.configure_input(self.input_channel.value, self.create_input_setup_settings())

    # creates this channels input setup settings from values set in InputData.py
    @abstract
    def create_input_setup_settings(self) -> Model372InputSetupSettings:
        raise NotImplementedError("Implement this method in subclass")
