from lakeshore import Model372
from Model372Mock import Model372Mock
import InputData


# Singleton of the Lakeshore Model

class Device:
    device = None
    ip_address = "192.168.0.12"
    DEBUG_MODE = True

    @staticmethod
    def get_device() -> Model372:
        if Device.DEBUG_MODE:
            return Model372Mock(baud_rate=None)

        if Device.device is None:
            try:
                Device.device = Model372(baud_rate=None, ip_address=Device.ip_address)
            except:
                print("couldn't connect to lakeshore\n"
                      "trying again ...")
                try:
                    Device.device = Model372(baud_rate=None, ip_address=Device.ip_address)
                except:
                    print("still couldn't connect to lakeshore\n"
                          "aborting process")

        return Device.device

