from lakeshore import Model372
import InputData
from Channel import Channel
from src.Device import Device
from src.Datahub import Datahub
from src.Heater import Heater
from src.Thermometer import Thermometer
from src.Channel import Channel, ChannelSettings
from MPVWrapper import MPVWrapper, MPVSettings
import src.Gui as Gui


class Controller:

    def __init__(self):
        self.channels = []
        self.mpv_wrapper = None
        self.ready = False
        self.logging_interval = 5
        print(self)
        Gui.show_gui(self)
        # self.heater = Heater(Device.get_device(), InputData.CHANNEL_HEATER)
        # self.thermometer = Thermometer(Device.get_device(), InputData.CHANNEL_THERMOMETER)
        # if InputData.MPV_ENABLED:
        #     self.mpv_wrapper = MPVWrapper()
        self.datahub = Datahub(channels=self.channels, mpv_wrapper=self.mpv_wrapper)

    # starts the process
    # TODO: set_scanner_status to relevant channel
    def start(self):
        if not self.ready:
            return

        print("starting process")
        self.datahub.start_logging(self.logging_interval)
        # try:
        #     self.datahub.start_logging(self.logging_interval)
        # except:
        #     print("something went wrong")
        #     self.datahub.write_csv(name="emergency_out")

    def create_channel(self, settings: ChannelSettings):
        self.channels.append(settings.create_channel(Device.get_device()))

    def create_mpv_wrapper(self, settings: MPVSettings):
        self.mpv_wrapper = settings.create_mpv_wrapper()


    # TODO: behaviour for stopping/exiting
