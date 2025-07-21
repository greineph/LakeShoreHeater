import os
import time
from threading import Thread
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
import sys

from lakeshore import Model372, Model372InputSetupSettings

from src import GuiHelper, FunctionalityFunctions
from src.AbstractFunctionality import AbstractFunctionality
from src.Device import Device
from src.InputData import range_text_converter
from src.SettingsGui import SettingsGui


class ActiveGui(qtw.QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.paused = False
        self.channels = []

        self.setGeometry(100, 100, 400, 0)
        # self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("  Active")
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png"))
        self.setWindowIcon(qtg.QIcon(path))

        self.setLayout(qtw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setFont(qtg.QFont("Bahnschrift", 16))
        self.setStyleSheet(" QToolTip{ font: 16pt }")
        self.setToolTipDuration(0)

        tabs = qtw.QTabWidget()
        self.layout().addWidget(tabs)

        # main tab
        main_tab = qtw.QWidget()
        self.load_main_tab(main_tab)
        tabs.addTab(main_tab, "Tab 1")

        settings_tab = qtw.QWidget()
        settings_tab.setLayout(qtw.QVBoxLayout())

        # channel tab
        channel_holder = qtw.QWidget()
        channel_holder.setLayout(qtw.QHBoxLayout())
        channel_holder.layout().setContentsMargins(0, 0, 0, 0)
        for ch in self.controller.channels:
            settings_holder = qtw.QWidget()
            self.load_channel_settings_form(settings_holder, ch.input_channel.value)
            channel_holder.layout().addWidget(settings_holder)
        settings_tab.layout().addWidget(channel_holder)

        apply_btn = qtw.QPushButton("Apply")
        apply_btn.setFont(qtg.QFont("Bahnschrift", 16))
        settings_tab.layout().addWidget(apply_btn)

        def apply_settings():
            for ch in self.channels:
                channel_settings = {}
                for item in ch.items():
                    channel_settings[item[0]] = GuiHelper.get_data_from_widget(item[1])
                settings = Model372InputSetupSettings(mode=channel_settings["mode"],
                                                      excitation_range=channel_settings["excitation_range"],
                                                      auto_range=channel_settings["auto_range"],
                                                      current_source_shunted=channel_settings["shunted"],
                                                      units=channel_settings["units"],
                                                      resistance_range=channel_settings["resistance_range"])
                Device.get_device().configure_input(channel_settings["input_channel"], settings)

        apply_btn.clicked.connect(apply_settings)
        tabs.addTab(settings_tab, "Settings")

        # functionality tab
        functionality_tab = qtw.QWidget()
        functionality_tab.setLayout(qtw.QVBoxLayout())

        functionality_holder = qtw.QWidget()
        functionality_holder.setLayout(qtw.QHBoxLayout())
        functionality_holder.layout().setContentsMargins(0, 0, 0, 0)
        for ch in self.controller.channels:
            settings_holder = qtw.QWidget()
            self.load_functionality_settings_(settings_holder, ch.functionality)
            functionality_holder.layout().addWidget(settings_holder)
        functionality_tab.layout().addWidget(functionality_holder)
        tabs.addTab(functionality_tab, "Functionality")

        tabs.setCurrentIndex(2)

        self.show()

    def load_main_tab(self, parent: qtw.QWidget):
        layout = qtw.QVBoxLayout()
        parent.setLayout(layout)
        parent.setFont(qtg.QFont("Bahnschrift", 16))

        # possibly unnecessary
        pause_unpause = qtw.QPushButton(parent)
        pause_unpause.setText("Pause")
        self.paused = False
        layout.addWidget(pause_unpause)

        def pause_unpause_logging():
            if self.paused:
                self.paused = False
                pause_unpause.setText("Pause")
                self.controller.unpause_logging()
            else:
                self.paused = True
                pause_unpause.setText("Unpause")
                self.controller.pause_logging()

        pause_unpause.clicked.connect(pause_unpause_logging)

        stop = qtw.QPushButton(parent)
        stop.setText("Stop")
        layout.addWidget(stop)

    # TODO: test type of variables in InputSetupSettings
    def load_channel_settings_form(self, parent, index):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)
        parent.setFont(qtg.QFont("Bahnschrift", 16))

        title = qtw.QLabel(f"Channel {index}:")
        form_layout.addRow(title)

        channel_form = {"input_channel": index}
        self.channels.append(channel_form)
        channel_settings = Device.get_device().get_input_setup_parameters(index)
        print(vars(channel_settings))

        mode = qtw.QComboBox(parent)
        mode.addItem("voltage", Model372.SensorExcitationMode.VOLTAGE)
        mode.addItem("current", Model372.SensorExcitationMode.CURRENT)
        mode.setCurrentIndex(channel_settings.mode)
        form_layout.addRow("Excitation Mode:", mode)
        channel_form["mode"] = mode

        excitation_range = qtw.QComboBox(parent)
        form_layout.addRow("Excitation Range:", excitation_range)
        channel_form["excitation_range"] = excitation_range

        auto_range = qtw.QComboBox(parent)
        auto_range.addItem("Off", Model372.AutoRangeMode.OFF)
        auto_range.addItem("On", Model372.AutoRangeMode.CURRENT)
        auto_range.setCurrentIndex(channel_settings.auto_range)
        form_layout.addRow("Auto Range:", auto_range)
        channel_form["auto_range"] = auto_range

        shunted = qtw.QCheckBox(parent)
        shunted.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
        shunted.setChecked(channel_settings.current_source_shunted)
        form_layout.addRow("Shunted:", shunted)
        channel_form["shunted"] = shunted

        units = qtw.QComboBox(parent)
        units.addItem("Kelvin", Model372.InputSensorUnits.KELVIN)
        units.addItem("Ohms", Model372.InputSensorUnits.OHMS)
        units.setCurrentIndex(channel_settings.units - 1)  # -1 because for no reason the enum starts at 1 and not 0 :|
        form_layout.addRow("Units:", units)
        channel_form["units"] = units

        resistance_range = qtw.QComboBox(parent)
        for x in Model372.MeasurementInputResistance:
            resistance_range.addItem(range_text_converter(x.name), x)
        resistance_range.setCurrentIndex(0 if index == "A" else channel_settings.resistance_range - 1)  # -1 because enum starts at 1, why?
        form_layout.addRow("Resistance Range:", resistance_range)
        if index == "A":
            resistance_range.setDisabled(True)
        channel_form["resistance_range"] = resistance_range

        def on_excitation_mode_changed(value):
            excitation_range.clear()
            print("changed ex mode")
            if value == Model372.SensorExcitationMode.CURRENT.value:
                if index == Model372.InputChannel.CONTROL.value:
                    for x in Model372.ControlInputCurrentRange:
                        excitation_range.addItem(range_text_converter(x.name), x)
                    excitation_range.setCurrentIndex(1)  # ControlInputCurrentRange.RANGE_1_NANO_AMP
                else:
                    for x in Model372.MeasurementInputCurrentRange:
                        excitation_range.addItem(range_text_converter(x.name), x)
                    excitation_range.setCurrentIndex(16)  # MeasurementInputCurrentRange.RANGE_100_MICRO_AMPS
            else:  # voltage TODO: sensible default value
                for x in Model372.MeasurementInputVoltageRange:
                    excitation_range.addItem(range_text_converter(x.name), x)

        mode.currentIndexChanged.connect(on_excitation_mode_changed)

        on_excitation_mode_changed(mode.currentData().value)
        excitation_range.setCurrentIndex(channel_settings.excitation_range - 1)  # -1 because bad enums (they start at 1)

    def load_functionality_settings_(self, parent, functionality):
        functionality.load_active_gui(parent)


def show_gui(controller):
    app = qtw.QApplication(sys.argv)
    gui = ActiveGui(controller)
    app.exec_()


# just for testing ui
if __name__ == "__main__":
    show_gui(None)
