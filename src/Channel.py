import Device
from lakeshore import Model372

class Channel:

    def __init__(self, device: Model372, input_channel: Model372.InputChannel):
        self.device = device
        self.input_channel = input_channel

    def get_readings(self):
        return self.device.get_all_input_readings(self.input_channel.value)