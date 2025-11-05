from simple_pid import PID


class PidController:

    def __init__(self, mpv, channel, tunings, interval):
        self.mpv = mpv
        self.channel = channel
        self.tunings = tunings
        self.interval = interval
        self.pid = PID()

    def execute(self):
        v = self.channel.last_reading["kelvin"]
        control = self.pid(v)
        self.mpv.set_ramp_rate(control)

