from enum import Enum

from lakeshore import Model372
from Model372Mock import Model372Mock
import InputData


# Singleton of the Lakeshore Model

class Device:
    device = None
    ip_address = "192.168.0.12"
    baud_rate = 57600
    mode = 0
    DEBUG_MODE = False

    @staticmethod
    def get_device() -> Model372:
        mode = Device.mode
        if Device.DEBUG_MODE:
            mode = ConnectionMode.DEBUG_MODE

        if Device.device is None:
            print(f"trying to connect to lakeshore using {mode.name}")
            try:
                Device.device = Device.connect(mode)
            except:
                print("couldn't connect to lakeshore\n"
                      "trying again ...")
                try:
                    Device.device = Device.connect(mode)
                except:
                    print("still couldn't connect to lakeshore\n"
                          "aborting process")

        return Device.device

    @staticmethod
    def connect(mode):
        match mode:
            case ConnectionMode.DEBUG_MODE:
                return Model372Mock(baud_rate=None)
            case ConnectionMode.IP_MODE:
                return Model372(baud_rate=None, ip_address=Device.ip_address)
            case ConnectionMode.USB_MODE:
                return Model372(baud_rate=Device.baud_rate)


class ConnectionMode(Enum):
    DEBUG_MODE = -1
    IP_MODE = 0
    USB_MODE = 1
