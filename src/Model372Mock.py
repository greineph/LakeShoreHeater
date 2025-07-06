from mimetypes import inited

from lakeshore import Model372, Model372InputSetupSettings


class Model372Mock(Model372):

    def __init__(self, baud_rate, **kwargs):
        try:
            super().__init__(baud_rate, **kwargs)
        except:
            print("DEBUG MODE IS ACTIVE")

    def get_all_input_readings(self, input_channel):
        return {"kelvin": 0,
                "resistance": 0,
                "power": 0,
                "quadrature": 0}

    def configure_input(self, input_channel, settings):
        pass

    def get_input_setup_parameters(self, input_channel):
        return Model372InputSetupSettings(0, 0, 0, False, 0, 0)

    def set_filter(self, input_channel, state, settle_time, window):
        pass

