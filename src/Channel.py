from Device import Device
from lakeshore import Model372, Model372InputSetupSettings
import InputData


class Channel:

    def __init__(self, device: Model372, input_channel: Model372.InputChannel):
        self.device = device
        self.input_channel = input_channel
        self.wanted_reading_keys = []
        self.wanted_reading_names = []
        self.wanted_plotting_names = []
        # self.configure_setup_settings()
        # self.set_filter()

    # returns readings of {kelvin, resistance, power} as dictionary
    def get_readings(self):
        return self.device.get_all_input_readings(self.input_channel.value)

    # configures channels setup settings in lakeshore device
    def configure_setup_settings(self, settings: Model372InputSetupSettings = None):
        if settings:
            self.device.configure_input(self.input_channel.value, settings)
        else:
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


# holds and processes all the relevant data defined in the settings menu
class ChannelSettings:

    def __init__(self, channel, excitation_mode, excitation_range, auto_range, shunted, units, resistance_range, readings):
        self.channel = channel
        self.excitation_mode = excitation_mode
        self.excitation_range = excitation_range
        self.auto_range = auto_range
        self.shunted = shunted
        self.units = units
        self.resistance_range = resistance_range
        self.readings = readings

    def create_input_setup_settings(self) -> Model372InputSetupSettings:
        return Model372InputSetupSettings(mode=self.excitation_mode,
                                          excitation_range=self.excitation_range,
                                          auto_range=self.auto_range,
                                          current_source_shunted=self.shunted,
                                          units=self.units,
                                          resistance_range=self.resistance_range)

    def create_channel(self, device) -> Channel:
        print("creating channel")
        channel = Channel(device=device, input_channel=self.channel)
        print("configuring settings")
        channel.configure_setup_settings(self.create_input_setup_settings())
        print("setting wanted stuff")
        channel.wanted_reading_keys = [reading["reading"] for reading in self.readings]
        print("keys")
        channel.wanted_reading_names = [reading["custom_name"] for reading in self.readings]
        print("names")
        channel.wanted_plotting_names = [reading["custom_name"] for reading in self.readings if reading["plot"]]
        print("done")

        return channel


    def __str__(self):
        return (f"{self.channel}: {self.excitation_mode}: {self.excitation_range}: {self.auto_range}: {self.shunted}: "
                f"{self.units}: {self.resistance_range}: {self.readings}")
