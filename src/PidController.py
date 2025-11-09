import time

from simple_pid import PID
import threading


class PidController:

    def __init__(self, mpv, channel, tunings, interval):
        self.mpv = mpv
        self.channel = channel
        self.tunings = tunings
        self.interval = interval
        self.pid = PID(1, 0.1, 0.05, setpoint=0)
        self.pid.output_limits = (0, 50)
        self.thread = None
        self.running = False

    def execute(self):
        v = self.channel.last_reading["kelvin"]
        control = self.pid(v)
        self.mpv.set_ramp_rate(control)

    def run(self):
        while self.running:
            self.execute()
            time.sleep(self.interval)

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
        self.running = True

    def stop(self):
        self.running = False

