from xlsxwriter.contenttypes import overrides

from Channel import Channel
from lakeshore import Model372InputSetupSettings
import InputData


class Heater(Channel):

    # creates input setup settings for heater from InputData.py
    # TODO: clarify other settings
    @overrides
    def create_input_setup_settings(self):
        return Model372InputSetupSettings(auto_range=InputData.AUTO_RANGE_MODE_THERMOMETER)

    # TODO: clarify which heater to use (sample, warm up, analog, other): channel heater for base functionality
    # other heaters for possible cryopump
    # TODO: clarify which setting "stromstärke" refers to
