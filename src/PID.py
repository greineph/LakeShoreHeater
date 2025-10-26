from simple_pid import PID


class PidController:

    def __init__(self, mpv, channel, tunings):
        self.mpv = mpv
        self.channel = channel
        self.tunings = tunings
