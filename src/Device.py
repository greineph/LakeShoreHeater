from lakeshore import Model372
import InputData


# Singleton of the Lakeshore Model

class Device:
    device = None

    @staticmethod
    def get_device() -> Model372:
        if Device.device is None:
            Device.device = Model372(baud_rate=None, ip_address=InputData.IP_ADDRESS)

        return Device.device

