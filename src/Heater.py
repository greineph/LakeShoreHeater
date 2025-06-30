from Channel import Channel
from lakeshore import Model372InputSetupSettings
import InputData
from src.InputData import SENSOR_EXCITATION_MODE_HEATER

# [deprecated]
class Heater(Channel):

    # creates input setup settings for heater from InputData.py
    def create_input_setup_settings(self):
        return Model372InputSetupSettings(mode=InputData.SENSOR_EXCITATION_MODE_HEATER,
                                          excitation_range=InputData.EXCITATION_RANGE_HEATER,
                                          auto_range=InputData.AUTO_RANGE_MODE_HEATER,
                                          current_source_shunted=InputData.CURRENT_SOURCE_SHUNTED_HEATER,
                                          units=InputData.UNITS_HEATER,
                                          resistance_range=InputData.RESISTANCE_RANGE_HEATER)

    # gets the selected readings from InputData
    # @override
    def get_wanted_reading_keys(self) -> list[str]:
        return InputData.WANTED_READINGS_HEATER
