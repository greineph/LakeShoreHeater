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
from src.MPVWrapper import MPVWrapper


class HeaterFunctionality(AbstractFunctionality):

    def __init__(self, use_threshold, activation_threshold, deactivation_threshold,
                 use_stability, number_of_values, deviation, max_threshold, active_excitation, interval):
        super().__init__()
        self.heater_active = False
        self.mpv_wrapper = None
        self.thread = None
        self.is_running = False
        self.automatic = True

        self.use_threshold = use_threshold
        self.current_value = np.nan
        self.activation_threshold = activation_threshold
        self.deactivation_threshold = deactivation_threshold
        # self.threshold_delta = threshold_delta

        self.use_stability = use_stability
        self.number_of_values = number_of_values if use_stability else 1
        self.recent_values = []
        self.deviation = deviation
        self.max_threshold = max_threshold

        self.active_excitation = active_excitation
        self.idle_excitation = None
        self.interval = interval

        # gui elements
        self.active_display = None
        self.toggle_active = None

    def start(self):
        print("start functionality of heater")
        print(self.mpv_wrapper)
        self.is_running = True

        def run(heater: HeaterFunctionality, mpv_wrapper: MPVWrapper):
            start_time = time.monotonic()
            while heater.is_running:
                heater.add_value(mpv_wrapper.get_field())
                if heater.automatic:
                    heater.update()
                time.sleep(heater.interval - ((time.monotonic() - start_time) % heater.interval))

        self.thread = threading.Thread(target=run, args=(self, self.mpv_wrapper), daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False

    # activates/deactivates the heater based on criteria set during initialisation
    def update(self):
        # print("heater automatic tick")
        if self.use_threshold:
            if self.current_value <= self.activation_threshold:
                self.activate_heater()
            elif self.current_value >= self.deactivation_threshold:
                self.deactivate_heater()

        elif self.use_stability:
            time_based_deviation = self.calculate_time_based_deviation()
            if (time_based_deviation <= self.deviation and self.current_value < self.max_threshold and
                    len(self.recent_values) == self.number_of_values):
                self.activate_heater()
            elif time_based_deviation > self.deviation:
                self.deactivate_heater()

    # add a new value to be used in update
    def add_value(self, value):
        self.current_value = value
        self.recent_values.append(value)
        if len(self.recent_values) > self.number_of_values:
            self.recent_values.remove(self.recent_values[0])
        # print(f"recent vals: {self.recent_values}")

    # calculates relative deviation from recent values
    def calculate_time_based_deviation(self):
        deviations = [0]
        for i in range(1, len(self.recent_values)):
            deviations.append((self.recent_values[0] - self.recent_values[i]) / (self.interval * i))

        print(abs(sum(deviations) / len(deviations)))
        return abs(sum(deviations) / len(deviations))

    # activates the heater of associated channel by changing excitation range
    def activate_heater(self, override=False):
        if self.heater_active and override:
            return

        print("activating heater")
        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.active_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = True
        self.update_gui_elements()

    # deactivates the heater of associated channel by changing excitation range
    def deactivate_heater(self):
        if not self.heater_active:
            return

        print("deactivating heater")
        settings = self.channel.get_setup_settings()
        settings.excitation_range = self.idle_excitation
        self.channel.configure_setup_settings(settings)
        self.heater_active = False
        self.update_gui_elements()

    def add_channel(self, channel):
        self.channel = channel
        self.idle_excitation = channel.get_setup_settings().excitation_range

    def provide_dependencies(self, controller):
        self.mpv_wrapper = controller.mpv_wrapper
        print(controller.mpv_wrapper)

    def change_settings(self, settings):
        self.use_threshold = settings["threshold"]
        self.activation_threshold = settings["activation"]
        self.deactivation_threshold = settings["deactivation"]
        self.use_stability = settings["stability"]
        self.number_of_values = settings["values"]
        self.deviation = settings["deviation"]
        self.max_threshold = settings["max"]
        self.active_excitation = settings["active"]
        if self.heater_active:
            self.activate_heater(override=True)
        self.interval = settings["interval"]

    def update_gui_elements(self):
        if self.active_display:
            self.active_display.setText("● active" if self.heater_active else "● inactive")
            self.active_display.setStyleSheet(f"color: {'green' if self.heater_active else 'red'}")

        if self.toggle_active:
            self.toggle_active.setText("Deactivate" if self.heater_active else "Activate")

    def load_active_gui(self, parent):
        parent.setLayout(qtw.QVBoxLayout())
        parent.setFont(qtg.QFont("Bahnschrift", 16))
        title_holder = qtw.QWidget()
        title_holder.setLayout(qtw.QHBoxLayout())
        title_holder.layout().addWidget(qtw.QLabel("Heater"))
        self.active_display = qtw.QLabel("● active" if self.heater_active else "● inactive")
        self.active_display.setStyleSheet(f"color: {'green' if self.heater_active else 'red'}")
        self.active_display.setFont(qtg.QFont("Bahnschrift", 16))
        title_holder.layout().addWidget(self.active_display)
        parent.layout().addWidget(title_holder)
        form_holder = qtw.QWidget()
        form_holder.setLayout(qtw.QFormLayout())
        form = load_gui_elements(form_holder)
        parent.layout().addWidget(form_holder)

        apply_btn = qtw.QPushButton("Apply")
        parent.layout().addWidget(apply_btn)

        toggle_auto = qtw.QPushButton("Set Manual")
        parent.layout().addWidget(toggle_auto)

        def toggle_heater_automation():
            if self.automatic:
                self.automatic = False
                toggle_auto.setText("Set Automatic")
            else:
                self.automatic = True
                toggle_auto.setText("Set Manual")

        toggle_auto.clicked.connect(toggle_heater_automation)

        self.toggle_active = qtw.QPushButton("Deactivate" if self.heater_active else "Activate")
        parent.layout().addWidget(self.toggle_active)

        def toggle_heater_active():
            if self.heater_active:
                self.deactivate_heater()
            else:
                self.activate_heater()

        self.toggle_active.clicked.connect(toggle_heater_active)

        def apply_settings():
            data = extract_data(form)
            print(data)
            self.change_settings(data)
            print(self.use_stability)

        apply_btn.clicked.connect(apply_settings)


def load_gui_elements(parent: qtw.QWidget):
    layout = parent.layout()
    form = {}
    if not isinstance(layout, qtw.QFormLayout):
        return form

    use_threshold = qtw.QCheckBox(parent)
    use_threshold.setChecked(True)
    layout.addRow("Threshold", use_threshold)
    form["threshold"] = use_threshold

    activation_threshold = qtw.QSpinBox()
    activation_threshold.setRange(0, 200000)
    activation_threshold.setValue(100)
    activation_threshold.setSuffix(" Oe")
    activation_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    activation_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Activates at:", activation_threshold)
    form["activation"] = activation_threshold

    deactivation_threshold = qtw.QSpinBox()
    deactivation_threshold.setRange(0, 200000)
    deactivation_threshold.setValue(500)
    deactivation_threshold.setSuffix(" Oe")
    deactivation_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    deactivation_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Deactivates at:", deactivation_threshold)
    form["deactivation"] = deactivation_threshold

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
    deviation.setSuffix(" Oe/s")
    deviation.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    deviation.setAlignment(Qt.AlignRight)
    layout.addRow("Deviation:", deviation)
    form["deviation"] = deviation

    max_threshold = qtw.QSpinBox()
    max_threshold.setRange(0, 200000)
    max_threshold.setValue(50000)
    max_threshold.setSuffix(" Oe")
    max_threshold.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    max_threshold.setAlignment(Qt.AlignRight)
    layout.addRow("Max Threshold:", max_threshold)
    form["max"] = max_threshold

    active_excitation = qtw.QComboBox(parent)
    for x in Model372.MeasurementInputCurrentRange:
        active_excitation.addItem(range_text_converter(x.name), x)
    active_excitation.setCurrentIndex(16)                    # MeasurementInputCurrentRange.RANGE_100_MICRO_AMPS
    layout.addRow("Active Excitation:", active_excitation)
    form["active"] = active_excitation

    interval = qtw.QDoubleSpinBox()
    interval.setRange(1, 100)
    interval.setValue(2)
    interval.setSuffix(" s")
    interval.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
    interval.setAlignment(Qt.AlignRight)
    layout.addRow("Interval:", interval)
    form["interval"] = interval

    def on_use_threshold_change(checked=False):
        if checked:
            use_stability.setChecked(False)
            activation_threshold.setEnabled(True)
            deactivation_threshold.setEnabled(True)
        else:
            activation_threshold.setEnabled(False)
            deactivation_threshold.setEnabled(False)

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
                               use_stability=data["stability"],
                               number_of_values=data["values"],
                               deviation=data["deviation"],
                               max_threshold=data["max"],
                               active_excitation=data["active"],
                               interval=data["interval"])
