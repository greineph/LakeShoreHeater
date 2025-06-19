import numpy as np
from PyQt5 import QtWidgets as qtw


class HeaterFunctionality:

    def __init__(self, channel, use_threshold, activation_threshold, deactivation_threshold, threshold_delta,
                 use_stability, number_of_values, deviation, max_threshold, active_excitation, inactive_excitation,
                 interval):
        self.channel = channel
        self.heater_active = False

        self.use_threshold = use_threshold
        self.current_value = 9999.9
        self.activation_threshold = activation_threshold
        self.deactivation_threshold = deactivation_threshold
        self.threshold_delta = threshold_delta

        self.use_stability = use_stability
        self.number_of_values = number_of_values
        self.recent_values = []
        self.deviation = deviation
        self.max_threshold = max_threshold

        self.active_excitation = active_excitation
        self.inactive_excitation = inactive_excitation
        self.interval = interval

    # activates/deactivates the heater based on criteria set during initialisation
    def update(self):
        if self.use_threshold:
            if self.current_value < self.activation_threshold + self.threshold_delta:
                self.activate_heater()
            elif self.current_value > self.deactivation_threshold - self.threshold_delta:
                self.deactivate_heater()

        elif self.use_stability:
            std = np.std(self.recent_values)
            if std < self.deviation and self.current_value < self.max_threshold:
                self.activate_heater()
            elif std > self.deviation:
                self.deactivate_heater()

    # add a new value to be used in update
    def add_value(self, value):
        self.recent_values.append(value)
        if len(self.recent_values) > self.number_of_values:
            self.recent_values.remove(self.recent_values[0])

    # activates the heater of associated channel by changing excitation range
    def activate_heater(self):
        if self.heater_active:
            return

        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.active_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = True

    # deactivates the heater of associated channel by changing excitation range
    def deactivate_heater(self):
        if not self.heater_active:
            return

        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.inactive_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = False


def load_gui_elements(parent):
    layout = parent.layout()
    use_threshold = qtw.QCheckBox(parent)
    use_threshold.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
    layout.addRow("Threshold:", use_threshold)
