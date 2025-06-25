import time

import numpy as np
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt
from lakeshore import Model372
import threading

import src.GuiHelper as GuiHelper
from src.AbstractFunctionality import AbstractFunctionality
from src.InputData import range_text_converter


class HeaterFunctionality(AbstractFunctionality):

    def __init__(self, use_threshold, activation_threshold, deactivation_threshold, threshold_delta,
                 use_stability, number_of_values, deviation, max_threshold, active_excitation, interval):
        super().__init__()
        self.heater_active = False
        self.mpv_wrapper = None
        self.thread = None
        self.is_running = False

        self.use_threshold = use_threshold
        self.current_value = np.nan
        self.activation_threshold = activation_threshold
        self.deactivation_threshold = deactivation_threshold
        self.threshold_delta = threshold_delta

        self.use_stability = use_stability
        self.number_of_values = number_of_values if use_stability else 1
        self.recent_values = []
        self.deviation = deviation
        self.max_threshold = max_threshold

        self.active_excitation = active_excitation
        self.idle_excitation = None
        self.interval = interval

    def start(self):
        print("start functionality of heater")
        print(self.mpv_wrapper)
        self.is_running = True
        def run(heater: HeaterFunctionality, mpv_wrapper):
            start_time = time.monotonic()
            while heater.is_running:
                heater.add_value(mpv_wrapper.get_readings()["field"])
                heater.update()
                time.sleep(heater.interval - ((time.monotonic() - start_time) % heater.interval))


        self.thread = threading.Thread(target=run, args=(self, self.mpv_wrapper))
        self.thread.start()


    def stop(self):
        self.is_running = False

    # activates/deactivates the heater based on criteria set during initialisation
    def update(self):
        if self.use_threshold:
            if self.current_value < self.activation_threshold + self.threshold_delta:
                self.activate_heater()
            elif self.current_value > self.deactivation_threshold - self.threshold_delta:
                self.deactivate_heater()

        elif self.use_stability:
            std = np.std(self.recent_values)
            if std < self.deviation and self.current_value < self.max_threshold and len(self.recent_values) == self.number_of_values:
                self.activate_heater()
            elif std > self.deviation:
                self.deactivate_heater()

    # add a new value to be used in update
    def add_value(self, value):
        self.current_value = value
        self.recent_values.append(value)
        if len(self.recent_values) > self.number_of_values:
            self.recent_values.remove(self.recent_values[0])
        print(f"recent vals: {self.recent_values}")

    # activates the heater of associated channel by changing excitation range
    def activate_heater(self):
        if self.heater_active:
            return

        print("activating heater")
        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.active_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = True

    # deactivates the heater of associated channel by changing excitation range
    def deactivate_heater(self):
        if not self.heater_active:
            return

        print("deactivating heater")
        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.idle_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = False

    def add_channel(self, channel):
        self.channel = channel
        self.idle_excitation = channel.get_setup_settings().excitation_range

    def provide_dependencies(self, controller):
        self.mpv_wrapper = controller.mpv_wrapper
        print(controller.mpv_wrapper)


def load_gui_elements(parent: qtw.QWidget):
    print("loading elements")
    layout = parent.layout()
    form = {}
    if not isinstance(layout, qtw.QFormLayout):
        return form

    use_threshold = qtw.QCheckBox(parent)
    use_threshold.setChecked(True)
    layout.addRow("Threshold", use_threshold)
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


def extract_data(gui_elements):
    data = {}
    for key in gui_elements.keys():
        data[key] = GuiHelper.get_data_from_widget(gui_elements[key])
    return data


def create_instance(data):
    return HeaterFunctionality(use_threshold=data["threshold"],
                               activation_threshold=data["activation"],
                               deactivation_threshold=data["deactivation"],
                               threshold_delta=data["delta"],
                               use_stability=data["stability"],
                               number_of_values=data["values"],
                               deviation=data["deviation"],
                               max_threshold=data["max"],
                               active_excitation=data["active"],
                               interval=data["interval"])
