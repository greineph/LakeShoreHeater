import time

from simple_pid import PID
import threading
from PyQt5 import QtGui as qtg


class PidController:

    def __init__(self, mpv, channel, tunings=(-1000, -10, -0), target=1, max_rate=50, interval=1):
        self.mpv = mpv
        self.channel = channel
        self.tunings = tunings
        self.target = target
        self.max_rate = max_rate
        self.interval = interval
        self.pid = PID(*self.tunings, setpoint=self.target)
        self.pid.output_limits = (-max_rate, max_rate)
        self.pid.sample_time = interval
        self.thread = None
        self.is_running = False
        self.active_display = None
        self.display_ramp_rate = 0

        print(self)

    def execute(self):
        if self.mpv.get_field() <= 20:
            self.stop()
            return
        v = self.channel.last_reading["kelvin"]
        control = self.pid(v)
        self.mpv.set_ramp_rate(max(0.0, control))
        self.display_ramp_rate = control
        self.update_active_display()

    def run(self):
        while self.is_running:
            self.execute()
            time.sleep(self.interval)

    def start(self, start_value=None):
        self.is_running = True
        self.update_active_display()
        if start_value is not None:
            print(f"setting last output to: {start_value}")
            self.pid.set_auto_mode(enabled=False)
            self.pid.set_auto_mode(enabled=True, last_output=start_value)

        if self.thread is None or not self.thread.is_alive():
            print("starting new thread")
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.update_active_display()

    def change_settings(self, tunings, target):
        self.pid.tunings = tunings
        self.pid.setpoint = target

    def update_active_display(self):
        if not self.active_display:
            print("no active display found")
            return
        self.active_display.setText(("● active" if self.is_running else "● inactive")
                                    + f" ({self.display_ramp_rate:+.4f} Oe/sec)")
        self.active_display.setStyleSheet(f"color: {'green' if self.is_running else 'red'}")
        self.active_display.setFont(qtg.QFont("Bahnschrift", 16))

    def __str__(self):
        return (f"Source:  {self.channel.input_channel}\n" +
                f"Tunings: {self.tunings}\n" +
                f"Target:  {self.target}\n" +
                f"Rate:    {self.max_rate}")

