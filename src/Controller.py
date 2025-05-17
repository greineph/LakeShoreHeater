from lakeshore import Model372
import InputData
from Channel import Channel
from src.Device import Device
from src.Datahub import Datahub
from src.Heater import Heater
from src.Thermometer import Thermometer


class Controller:

    def __init__(self):
        self.heater = Heater(Device.get_device(), InputData.CHANNEL_HEATER)
        self.thermometer = Thermometer(Device.get_device(), InputData.CHANNEL_THERMOMETER)
        self.datahub = Datahub([self.heater, self.thermometer])

        self.start()

    # starts the process
    # TODO: set_scanner_status to relevant channel

    def start(self):
        print("starting process")
        self.datahub.start_logging()

    # TODO: get readings from multipyvu possibly in new class

    # TODO: behaviour for stopping/exiting
