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
from src.LiveGraph import Operations
from src.SettingsGui import SettingsGui


class ActiveGui(qtw.QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.paused = False
        self.channels = []
        self.queue = self.controller.datahub.queue if controller else None
        self.pid_controller = self.controller.pid_controller if controller else None
        self.graphs = {}

        self.setGeometry(100, 100, 400, 0)
        # self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("  Active")
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png"))
        self.setWindowIcon(qtg.QIcon(path))

        self.setLayout(qtw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setFont(qtg.QFont("Bahnschrift", 16))
        # self.setStyleSheet(" QToolTip{ font: 16pt }")
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
        for ch in (self.controller.channels if self.controller else []):
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
        for ch in (self.controller.channels if self.controller else []):
            settings_holder = qtw.QWidget()
            self.load_functionality_settings(settings_holder, ch.functionality)
            functionality_holder.layout().addWidget(settings_holder)
        functionality_tab.layout().addWidget(functionality_holder)
        tabs.addTab(functionality_tab, "Functionality")

        # graph tab
        graph_tab = qtw.QWidget()
        graph_tab.setLayout(qtw.QVBoxLayout())

        graph_holder = qtw.QWidget()
        self.load_graph_tab(graph_holder)
        graph_tab.layout().addWidget(graph_holder)
        tabs.addTab(graph_tab, "LiveGraph")

        # mpv tab
        mpv_tab = qtw.QWidget()
        mpv_tab.setLayout(qtw.QVBoxLayout())
        self.pid_active_display = qtw.QLabel()

        mpv_holder = qtw.QWidget()
        self.load_mpv_tab(mpv_holder)
        mpv_tab.layout().addWidget(mpv_holder)
        tabs.addTab(mpv_tab, "MPV")

        tabs.setCurrentIndex(3)

        self.show()

    def closeEvent(self, event):
        dialog = qtw.QDialog(self)
        dialog.setWindowTitle("Are you sure?")
        dialog.setLayout(qtw.QVBoxLayout())
        dialog.layout().setContentsMargins(30, 30, 30, 30)

        label = qtw.QLabel("Do you want to Exit?")
        label.setFont(qtg.QFont("Bahnschrift", 16))
        dialog.layout().addWidget(label)

        btn_holder = qtw.QWidget()
        btn_holder.setLayout(qtw.QHBoxLayout())
        btn_holder.layout().setContentsMargins(0, 0, 0, 0)
        btn_holder.setFont(qtg.QFont("Bahnschrift", 16))
        yes = qtw.QPushButton("Yes")
        btn_holder.layout().addWidget(yes)
        no = qtw.QPushButton("No")
        btn_holder.layout().addWidget(no)
        dialog.layout().addWidget(btn_holder)

        dialog.exec()
        event.ignore()

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

        resistance_range = qtw.QComboBox()
        for x in Model372.MeasurementInputResistance:
            resistance_range.addItem(range_text_converter(x.name), x)
        resistance_range.setCurrentIndex(
            0 if index == "A" else channel_settings.resistance_range - 1)  # -1 because enum starts at 1, why?
        if index != "A":
            form_layout.addRow("Resistance Range:", resistance_range)
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
        excitation_range.setCurrentIndex(
            channel_settings.excitation_range - 1)  # -1 because bad enums (they start at 1)

    def load_functionality_settings(self, parent, functionality):
        functionality.load_active_gui(parent)

    def load_graph_tab(self, parent: qtw.QWidget):
        layout = qtw.QVBoxLayout()
        parent.setLayout(layout)
        parent.setFont(qtg.QFont("Bahnschrift", 16))

        auto_xlim = qtw.QCheckBox("Auto adjust X-Axis", parent)
        auto_xlim.setChecked(True)
        layout.addWidget(auto_xlim)

        auto_ylim = qtw.QCheckBox("Auto adjust Y-Axis", parent)
        layout.addWidget(auto_ylim)

        centre_graph = qtw.QPushButton("Centre Graph")
        layout.addWidget(centre_graph)

        def on_change_auto_lim(state: int, axis: str):
            print(f"{axis}-axis is set to {bool(state)}")
            if self.queue is None:
                return

            if axis == "x":
                op = Operations.ENABLE_XLIM if state else Operations.DISABLE_XLIM
            else:
                op = Operations.ENABLE_YLIM if state else Operations.DISABLE_YLIM
            self.queue.put(["op", op])

        auto_xlim.stateChanged.connect(lambda s, a="x": on_change_auto_lim(s, a))
        auto_ylim.stateChanged.connect(lambda s, a="y": on_change_auto_lim(s, a))

        reading_names = []
        plotting_names = []
        for ch in (self.controller.channels if self.controller else []):
            reading_names += ch.wanted_reading_names
            plotting_names += ch.wanted_plotting_names
        if self.controller:
            reading_names += self.controller.mpv_wrapper.wanted_reading_names
            plotting_names += self.controller.mpv_wrapper.wanted_plotting_names

        def on_change_graph(state: int, key: str):
            self.graphs[key] = bool(state)
            print(self.graphs)
            print([x for x in reading_names if self.graphs[x]])
            if self.queue:
                self.queue.put(["op", Operations.CHANGE_DISPLAYED_GRAPHS, [x for x in reading_names if self.graphs[x]]])

        for col in reading_names:
            graph = qtw.QCheckBox(col, parent)
            visible = col in plotting_names
            graph.setChecked(visible)
            self.graphs[col] = visible
            layout.addWidget(graph)
            graph.stateChanged.connect(lambda s, k=col: on_change_graph(s, k))

        centre_graph.clicked.connect(lambda: self.queue.put(["op", Operations.CENTRE_GRAPHS]))

    def load_mpv_tab(self, parent: qtw.QWidget):
        layout = qtw.QFormLayout()
        parent.setLayout(layout)
        parent.setFont(qtg.QFont("Bahnschrift", 16))

        tuning1 = qtw.QLineEdit()
        tuning1.setAlignment(Qt.AlignCenter)
        tuning1.setPlaceholderText("Kp")
        layout.addRow("t1", tuning1)
        tuning2 = qtw.QLineEdit()
        tuning2.setAlignment(Qt.AlignCenter)
        tuning2.setPlaceholderText("Ki")
        layout.addRow("t2", tuning2)
        tuning3 = qtw.QLineEdit()
        tuning3.setAlignment(Qt.AlignCenter)
        tuning3.setPlaceholderText("Kd")
        layout.addRow("t3", tuning3)
        if self.pid_controller:
            tuning1.setText(str(self.pid_controller.tunings[0]))
            tuning2.setText(str(self.pid_controller.tunings[1]))
            tuning3.setText(str(self.pid_controller.tunings[2]))
        setpoint = qtw.QLineEdit()
        setpoint.setAlignment(Qt.AlignCenter)
        setpoint.setText("0")
        layout.addRow("setpoint", setpoint)
        apply_btn = qtw.QPushButton("Apply")
        layout.addRow("", apply_btn)
        layout.addRow("", qtw.QLabel(""))

        if self.pid_controller:
            self.pid_active_display = qtw.QLabel("● active" if self.pid_controller.is_running else "● inactive")
            self.pid_active_display.setStyleSheet(f"color: {'green' if self.pid_controller.is_running else 'red'}")
            self.pid_active_display.setFont(qtg.QFont("Bahnschrift", 16))
        layout.addRow(self.pid_active_display)
        start_holder = qtw.QWidget()
        start_holder.setLayout(qtw.QHBoxLayout())
        start_holder.layout().setContentsMargins(0, 0, 0, 0)
        start_btn = qtw.QPushButton("Start")
        start_holder.layout().addWidget(start_btn)
        start_value = qtw.QLineEdit()
        start_value.setAlignment(Qt.AlignCenter)
        start_value.setPlaceholderText("start at")
        start_holder.layout().addWidget(start_value)
        layout.addRow(start_holder)
        stop_btn = qtw.QPushButton("Stop")
        layout.addRow(stop_btn)

        def apply_settings():
            try:
                tunings = (float(GuiHelper.get_data_from_widget(tuning1)),
                           float(GuiHelper.get_data_from_widget(tuning2)),
                           float(GuiHelper.get_data_from_widget(tuning3)))
                setpoint_val = float(GuiHelper.get_data_from_widget(setpoint))
                print(f"{tunings}, {setpoint_val}")
                self.pid_controller.change_settings(tunings, setpoint_val)
            except ValueError:
                print("couldn't convert inputs to floats")
            except AttributeError:
                print("no pid_controller available")

        apply_btn.clicked.connect(apply_settings)

        def update_active_display():
            print(f"updating display with: {self.pid_controller.is_running}")
            self.pid_active_display.setText("● active" if self.pid_controller.is_running else "● inactive")
            self.pid_active_display.setStyleSheet(f"color: {'green' if self.pid_controller.is_running else 'red'}")
            self.pid_active_display.setFont(qtg.QFont("Bahnschrift", 16))

        def start_pid():
            try:
                start_val = float(GuiHelper.get_data_from_widget(start_value))
            except ValueError:
                print("no valid start value")
                start_val = None
            print("starting pid")
            self.pid_controller.start(start_val)
            update_active_display()

        start_btn.clicked.connect(start_pid)

        def stop_pid():
            print("stopping pid")
            self.pid_controller.stop()
            update_active_display()

        stop_btn.clicked.connect(stop_pid)



def show_gui(controller):
    app = qtw.QApplication(sys.argv)
    gui = ActiveGui(controller)
    app.exec_()


# just for testing ui
if __name__ == "__main__":
    show_gui(None)
