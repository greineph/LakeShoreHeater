from lakeshore import Model372
import InputData
from Channel import Channel
from src.Device import Device
from src.Datahub import Datahub
from src.Heater import Heater
from src.Thermometer import Thermometer
from src.Channel import Channel, ChannelSettings
from MPVWrapper import MPVWrapper, MPVSettings
import src.SettingsGui as Gui


class Controller:

    def __init__(self):
        self.channels = []
        self.mpv_wrapper = None
        self.ready = False
        self.logging_interval = 5
        self.save_path = ""
        Gui.show_gui(self)
        self.datahub = Datahub(channels=self.channels, mpv_wrapper=self.mpv_wrapper, save_path=self.save_path)

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
