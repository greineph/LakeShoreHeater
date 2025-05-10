from xlsxwriter.contenttypes import overrides

from Channel import Channel
from lakeshore import Model372InputSetupSettings
import InputData


class Thermometer(Channel):

    # creates input setup settings for thermometer from InputData.py
    # TODO: clarify other settings
    @overrides
    def create_input_setup_settings(self):
        return Model372InputSetupSettings(mode=InputData.SENSOR_EXCITATION_MODE_THERMOMETER,
                                          auto_range=InputData.AUTO_RANGE_MODE_THERMOMETER)

