import time

from Device import Device
from lakeshore import Model372, Model372InputSetupSettings
import InputData
import TemperatureCalibration
from src.AbstractFunctionality import AbstractFunctionality


class Channel:

    SCANNER_SETTLE_TIME = 3

    def __init__(self, device: Model372, input_channel: Model372.InputChannel):
        self.device = device
        self.input_channel = input_channel
        self.wanted_reading_keys = []
        self.wanted_reading_names = []
        self.wanted_plotting_names = []
        self.calibration = "None"
        self.functionality = None

    # returns readings of {kelvin, resistance, power, quadrature(optional)} as dictionary
    def get_readings(self):
        if self.input_channel != Model372.InputChannel.CONTROL and self.device.get_scanner_status() != self.input_channel:
            self.device.set_scanner_status(self.input_channel.value, False)
            time.sleep(Channel.SCANNER_SETTLE_TIME)

        return self.device.get_all_input_readings(self.input_channel.value)

    # configures channels setup settings in lakeshore device
    def configure_setup_settings(self, settings: Model372InputSetupSettings = None):
        if settings:
            self.device.configure_input(self.input_channel.value, settings)

    # returns channels setup settings from lakeshore device
    def get_setup_settings(self) -> Model372InputSetupSettings:
        return self.device.get_input_setup_parameters(self.input_channel.value)

    def get_wanted_reading_keys(self) -> list[str]:
        return self.wanted_reading_keys

    def get_wanted_readings(self) -> list:
        readings = self.get_readings()
        if "resistance" in self.wanted_reading_keys:
            # print(f"original value: {readings['resistance']}")
            if self.calibration != "None":
                readings["kelvin"] = TemperatureCalibration.functions[self.calibration](readings["resistance"])
            # print(f"using {self.calibration}: {readings['resistance']}")
        return [readings[key] for key in self.wanted_reading_keys]

    def get_input_channel(self):
        return self.input_channel

    def add_functionality(self, functionality: AbstractFunctionality):
        self.functionality = functionality
        functionality.add_channel(self)

    def start_functionality(self):
        self.functionality.start()

    def stop_functionality(self):
        self.functionality.stop()


# holds and processes all the relevant data defined in the settings menu
class ChannelSettings:

    def __init__(self, channel, calibration, excitation_mode, excitation_range, auto_range, shunted, units,
                 resistance_range, readings):
        self.channel = channel
        self.calibration = calibration
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
        channel = Channel(device=device, input_channel=self.channel)
        channel.configure_setup_settings(self.create_input_setup_settings())
        channel.wanted_reading_keys = [reading["reading"] for reading in self.readings]
        channel.wanted_reading_names = [reading["custom_name"] for reading in self.readings]
        channel.wanted_plotting_names = [reading["custom_name"] for reading in self.readings if reading["plot"]]
        channel.calibration = self.calibration
        return channel

    def __str__(self):
        return (f"{self.channel}: {self.excitation_mode}: {self.excitation_range}: {self.auto_range}: {self.shunted}: "
                f"{self.units}: {self.resistance_range}: {self.readings}")
