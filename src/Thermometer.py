from xlsxwriter.contenttypes import overrides

from Channel import Channel
from lakeshore import Model372InputSetupSettings
import InputData


class Thermometer(Channel):

    # creates input setup settings for thermometer from InputData.py
    @overrides
    def create_input_setup_settings(self):
        return Model372InputSetupSettings(mode=InputData.SENSOR_EXCITATION_MODE_THERMOMETER,
                                          excitation_range=InputData.EXCITATION_RANGE_THERMOMETER,
                                          auto_range=InputData.AUTO_RANGE_MODE_THERMOMETER,
                                          current_source_shunted=InputData.CURRENT_SOURCE_SHUNTED_THERMOMETER,
                                          units=InputData.UNITS_THERMOMETER,
                                          resistance_range=InputData.RESISTANCE_RANGE_THERMOMETER)

