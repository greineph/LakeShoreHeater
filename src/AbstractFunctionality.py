
class AbstractFunctionality:

    def __init__(self):
        self.channel = None

    def start(self):
        pass

    def stop(self):
        pass

    def add_channel(self, channel):
        self.channel = channel

    def provide_dependencies(self, controller):
        pass


def load_gui_elements(parent):
    return {}


def extract_data(gui_elements):
    print("extract abstract data")
    return {}


def create_instance(data):
    print("create abstract instance")
    return AbstractFunctionality()
