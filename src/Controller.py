from lakeshore import Model372
import InputData
from Channel import Channel
from Device import Device


class Controller:

    def __init__ (self):
        self.heater = Channel(Device.get_device(), InputData.CHANNEL_HEATER)
        self.thermometer = Channel(Device.get_device(), InputData.CHANNEL_THERMOMETER)

    # starts the process
    # TODO: set_scanner_status to relevant channel

    def run(self):
        return

    # TODO: get readings from multipyvu possibly in new class

    # TODO: behaviour for stopping/exiting


