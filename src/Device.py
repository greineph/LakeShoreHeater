from lakeshore import Model372
import InputData


# Singleton of the Lakeshore Model

class Device:
    device = None

    @staticmethod
    def get_device() -> Model372:
        if Device.device is None:
            try:
                Device.device = Model372(baud_rate=None, ip_address=InputData.IP_ADDRESS)
            except:
                print("couldn't connect to lakeshore\n"
                      "trying again ...")
                try:
                    Device.device = Model372(baud_rate=None, ip_address=InputData.IP_ADDRESS)
                except:
                    print("still couldn't connect to lakeshore\n"
                          "aborting process")

        return Device.device

