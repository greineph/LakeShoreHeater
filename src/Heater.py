from xlsxwriter.contenttypes import overrides

from Channel import Channel
from lakeshore import Model372InputSetupSettings
import InputData
from src.InputData import SENSOR_EXCITATION_MODE_HEATER


class Heater(Channel):

    # creates input setup settings for heater from InputData.py
    @overrides
    def create_input_setup_settings(self):
        return Model372InputSetupSettings(mode=InputData.SENSOR_EXCITATION_MODE_HEATER,
                                          excitation_range=InputData.EXCITATION_RANGE_HEATER,
                                          auto_range=InputData.AUTO_RANGE_MODE_HEATER,
                                          current_source_shunted=InputData.CURRENT_SOURCE_SHUNTED_HEATER,
                                          units=InputData.UNITS_HEATER,
                                          resistance_range=InputData.RESISTANCE_RANGE_HEATER)

    # TODO: heaters (sample, warm up, analog, other): channel heater for base functionality other heaters for possible cryopump

    # TODO: enable/disable channel heater