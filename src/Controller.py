from lakeshore import Model372
import InputData
from Channel import Channel
from src.Device import Device
from src.Datahub import Datahub
from src.Heater import Heater
from src.Thermometer import Thermometer
from src.Channel import Channel, ChannelSettings
from MPVWrapper import MPVWrapper


class Controller:

    def __init__(self):
        self.channels = []
        self.heater = Heater(Device.get_device(), InputData.CHANNEL_HEATER)
        self.thermometer = Thermometer(Device.get_device(), InputData.CHANNEL_THERMOMETER)
        self.mpv_wrapper = None
        if InputData.MPV_ENABLED:
            self.mpv_wrapper = MPVWrapper()
        self.datahub = Datahub(channels=[self.heater, self.thermometer], mpv_wrapper=self.mpv_wrapper)

    # starts the process
    # TODO: set_scanner_status to relevant channel
    def start(self):
        print("starting process")
        try:
            self.datahub.start_logging()
        except:
            print("something went wrong")
            self.datahub.write_csv(name="emergency_out")

    def create_channel(self, settings: ChannelSettings):
        self.channels.append(settings.create_channel(Device.get_device()))
        print(self.channels)


    # TODO: behaviour for stopping/exiting
