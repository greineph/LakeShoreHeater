import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import Qt
from lakeshore import Model372

from src.AbstractFunctionality import AbstractFunctionality
from src.InputData import range_text_converter


class HeaterFunctionality(AbstractFunctionality):

    def __init__(self, channel, use_threshold, activation_threshold, deactivation_threshold, threshold_delta,
                 use_stability, number_of_values, deviation, max_threshold, active_excitation, interval):
        super().__init__(channel)
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
        self.idle_excitation = channel.get_setup_settings().excitation_range
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
        settings.excitation_range = self.idle_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = False


def load_gui_elements(parent):
    print("loading elements")
    layout = parent.layout()
    form = {}

    use_threshold = qtw.QCheckBox(parent)
    use_threshold.setChecked(True)
    layout.addRow("Threshold:", use_threshold)
    form["threshold"] = use_threshold

    activation_threshold = qtw.QDoubleSpinBox()
    activation_threshold.setRange(0, 10000)
    activation_threshold.setValue(1)
    activation_threshold.setSuffix("B")
    activation_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    activation_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Activates at:", activation_threshold)
    form["activation"] = activation_threshold

    deactivation_threshold = qtw.QDoubleSpinBox()
    deactivation_threshold.setRange(0, 10000)
    deactivation_threshold.setValue(100)
    deactivation_threshold.setSuffix("B")
    deactivation_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    deactivation_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Deactivates at:", deactivation_threshold)
    form["deactivation"] = deactivation_threshold

    threshold_delta = qtw.QDoubleSpinBox()
    threshold_delta.setRange(0, 100)
    threshold_delta.setValue(2)
    threshold_delta.setSuffix("B")
    threshold_delta.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    threshold_delta.setAlignment(Qt.AlignRight)
    layout.addRow("Delta:", threshold_delta)
    form["delta"] = threshold_delta

    use_stability = qtw.QCheckBox(parent)
    layout.addRow("Stability:", use_stability)
    form["stability"] = use_stability

    number_of_values = qtw.QSpinBox()
    number_of_values.setRange(0, 100)
    number_of_values.setValue(5)
    number_of_values.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    number_of_values.setAlignment(Qt.AlignRight)
    layout.addRow("Number of Values:", number_of_values)
    form["values"] = number_of_values

    deviation = qtw.QDoubleSpinBox()
    deviation.setRange(0, 100)
    deviation.setValue(3)
    deviation.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    deviation.setAlignment(Qt.AlignRight)
    layout.addRow("Deviation:", deviation)
    form["deviation"] = deviation

    max_threshold = qtw.QDoubleSpinBox()
    max_threshold.setRange(0, 10000)
    max_threshold.setValue(200)
    max_threshold.setSuffix("B")
    max_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    max_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Max Threshold:", max_threshold)
    form["max"] = max_threshold

    # TODO: change type depending on mode
    active_excitation = qtw.QComboBox(parent)
    for x in Model372.MeasurementInputCurrentRange:
        active_excitation.addItem(range_text_converter(x.name), x)
    layout.addRow("Active Excitation:", active_excitation)
    form["active"] = active_excitation

    interval = qtw.QDoubleSpinBox()
    interval.setRange(1, 100)
    interval.setValue(2)
    interval.setSuffix("s")
    interval.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    interval.setAlignment(Qt.AlignRight)
    layout.addRow("Interval:", interval)
    form["interval"] = interval

    def on_use_threshold_change(checked=False):
        if checked:
            use_stability.setChecked(False)
            activation_threshold.setEnabled(True)
            deactivation_threshold.setEnabled(True)
            threshold_delta.setEnabled(True)
        else:
            activation_threshold.setEnabled(False)
            deactivation_threshold.setEnabled(False)
            threshold_delta.setEnabled(False)

    use_threshold.stateChanged.connect(on_use_threshold_change)

    def on_use_stability_change(checked=False):
        if checked:
            use_threshold.setChecked(False)
            number_of_values.setEnabled(True)
            deviation.setEnabled(True)
            max_threshold.setEnabled(True)
        else:
            number_of_values.setEnabled(False)
            deviation.setEnabled(False)
            max_threshold.setEnabled(False)

    use_stability.stateChanged.connect(on_use_stability_change)
    on_use_stability_change(False)

    return form


# TODO: implement
def extract_data(gui_elements):
    pass


# TODO: implement
def create_instance(channel, data):
    pass
