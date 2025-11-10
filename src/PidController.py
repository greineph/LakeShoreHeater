import time

from simple_pid import PID
import threading


class PidController:

    def __init__(self, mpv, channel, tunings=(-1, -0.1, -0.05), interval=1):
        self.mpv = mpv
        self.channel = channel
        self.tunings = tunings
        self.interval = interval
        self.pid = PID(*self.tunings, setpoint=0)
        self.pid.output_limits = (-50, 50)
        self.pid.sample_time = interval
        self.thread = None
        self.is_running = False

    def execute(self):
        v = self.channel.last_reading["kelvin"]
        control = self.pid(v)
        self.mpv.set_ramp_rate(abs(control))
        print(f"setting ramprate to: {control}")

    def run(self):
        while self.is_running:
            self.execute()
            time.sleep(self.interval)

    # TODO: implement start value
    def start(self, start_value=None):
        self.is_running = True
        if self.thread is None or not self.thread.is_alive():
            print("starting new thread")
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False

    def change_settings(self, tunings, setpoint):
        self.pid.tunings = tunings
        self.pid.setpoint = setpoint

