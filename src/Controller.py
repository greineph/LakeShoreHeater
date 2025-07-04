from threading import Thread

from lakeshore import Model372
import InputData
from Channel import Channel
from src.AbstractFunctionality import AbstractFunctionality
from src.Device import Device
from src.Datahub import Datahub
from src.Heater import Heater
from src.Thermometer import Thermometer
from src.Channel import Channel, ChannelSettings
from MPVWrapper import MPVWrapper, MPVSettings
import src.SettingsGui as SettingsGui
import src.ActiveGui as ActiveGui


class Controller:

    # TODO: error handling
    def __init__(self):
        self.channels = []
        self.mpv_wrapper = None
        self.ready = False
        self.logging_interval = 5
        self.save_path = ""
        self.append_to_file = False
        SettingsGui.show_gui(self)
        self.datahub = Datahub(channels=self.channels,
                               mpv_wrapper=self.mpv_wrapper,
                               save_path=self.save_path,
                               append_to_file=self.append_to_file,
                               controller=self)
        self.provide_dependencies()

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

    def pause_logging(self):
        self.datahub.pause_logging()

    def unpause_logging(self):
        self.datahub.unpause_logging()

    def create_channel(self, settings: ChannelSettings, functionality: AbstractFunctionality):
        channel = settings.create_channel(Device.get_device())
        channel.add_functionality(functionality)
        self.channels.append(channel)

    def create_mpv_wrapper(self, settings: MPVSettings):
        self.mpv_wrapper = settings.create_mpv_wrapper()

    def provide_dependencies(self):
        for ch in self.channels:
            ch.functionality.provide_dependencies(self)

    def show_active_gui(self):
        gui_thread = Thread(target=ActiveGui.show_gui, args=[self], daemon=True)
        gui_thread.start()
        print("gui started")


    # TODO: behaviour for stopping/exiting
