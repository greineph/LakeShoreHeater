import numpy as np


class HeaterFunctionality:

    def __init__(self):
        self.channel = None
        self.heater_active = False

        self.use_threshold = False
        self.current_value = 0
        self.activation_threshold = 1
        self.deactivation_threshold = 10
        self.threshold_delta = 0.5

        self.use_stability = False
        self.number_of_values = 10
        self.recent_values = []
        self.standard_deviation = 2
        self.max_threshold = 50

    def check(self):
        if self.use_threshold:
            if self.current_value < self.activation_threshold + self.threshold_delta:
                self.activate_heater()
            elif self.current_value > self.deactivation_threshold - self.threshold_delta:
                self.deactivate_heater()

        elif self.use_stability:
            std = np.std(self.recent_values)
            if std < self.standard_deviation and self.current_value < self.max_threshold:
                self.activate_heater()
            elif std > self.standard_deviation:
                self.deactivate_heater()

    def add_value(self, value):
        self.recent_values.append(value)
        if len(self.recent_values) > self.number_of_values:
            self.recent_values.remove(self.recent_values[0])

    def activate_heater(self):
        if self.heater_active:
            return

        self.heater_active = True

    def deactivate_heater(self):
        if not self.heater_active:
            return

        self.heater_active = False

