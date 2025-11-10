from threading import Thread

from lakeshore import Model372
import InputData
from Channel import Channel
from src import TemperatureCalibration
from src.AbstractFunctionality import AbstractFunctionality
from src.Device import Device
from src.Datahub import Datahub
from src.TemperatureCalibrationGui import TemperatureCalibrationGui
from src.Thermometer import Thermometer
from src.Channel import Channel, ChannelSettings
from MPVWrapper import MPVWrapper, MPVSettings
from PidController import PidController
import src.SettingsGui as SettingsGui
import src.ActiveGui as ActiveGui


class Controller:

    # TODO: error handling
    def __init__(self):
        self.channels = []
        self.mpv_wrapper = None
        self.pid_controller = None
        self.ready = False
        self.logging_interval = 5
        self.save_path = ""
        self.append_to_file = False
        TemperatureCalibration.generate_functions_from_files()
        SettingsGui.show_gui(self)
        self.datahub = Datahub(channels=self.channels,
                               mpv_wrapper=self.mpv_wrapper,
                               save_path=self.save_path,
                               append_to_file=self.append_to_file,
                               controller=self)
        self.provide_dependencies()
        try:
            self.pid_controller = PidController(mpv=self.mpv_wrapper,
                                                channel=self.channels[0])
        except Exception:
            print("something wrong with pid instantiation")

    # starts the process
    def start(self):
        if not self.ready:
            return

        print("starting process")
        self.datahub.start_logging(self.logging_interval)
        ActiveGui.show_gui(self)

    def pause_logging(self):
        self.datahub.pause_logging()

    def unpause_logging(self):
        self.datahub.unpause_logging()

    def create_channel(self, settings: ChannelSettings, functionality: AbstractFunctionality):
        channel = settings.create_channel(Device.get_device())
        channel.add_functionality(functionality)
        self.channels.append(channel)

    def configure_lakeshore(self, ip, state, settle_time, window):
        Device.ip_address = ip
        print("setting filter")
        Device.get_device().set_filter(0, state, settle_time, window)
        print(Device.get_device().get_filter(1))

    def create_mpv_wrapper(self, settings: MPVSettings):
        self.mpv_wrapper = settings.create_mpv_wrapper()

    def provide_dependencies(self):
        for ch in self.channels:
            ch.functionality.provide_dependencies(self)

