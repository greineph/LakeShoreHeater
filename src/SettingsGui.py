import os
import time
from threading import Thread
import json
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
import sys

from InputData import range_text_converter
from Channel import ChannelSettings
from MPVWrapper import MPVSettings
from src import TemperatureCalibration, GuiHelper
import FunctionalityFunctions

from UliEngineering.Electronics.Resistors import resistor_tolerance
from lakeshore import Model372

from src.Device import Device


class SettingsGui(qtw.QWidget):

    def __init__(self, controller=None):
        super().__init__()

        self.controller = controller

        self.channel_forms = []
        self.lakeshore_form = {}
        self.mpv_form = {}
        self.logging_form = {}

        self.filename = "default.json"

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle("  Setup")
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png"))
        self.setWindowIcon(qtg.QIcon(path))

        self.setLayout(qtw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setFont(qtg.QFont("Bahnschrift", 16))
        self.setStyleSheet(" QToolTip{ font: 16pt }")
        self.setToolTipDuration(0)

        label = qtw.QLabel("Settings")
        title_font = qtg.QFont("Bahnschrift", 30)
        title_font.setBold(True)
        label.setFont(title_font)
        label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(label)

        form_holder_holder = qtw.QWidget()
        form_holder_holder.setLayout(qtw.QHBoxLayout())
        self.layout().addWidget(form_holder_holder)

        form_holder = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder)
        self.load_channel_settings_form(form_holder)

        form_holder2 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder2)
        self.load_channel_settings_form(form_holder2, index=1)

        form_holder3 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder3)
        self.load_mpv_settings_form(form_holder3)

        form_holder4 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder4)
        self.load_logging_settings_form(form_holder4)

        form_holder5 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder5)
        self.load_lakeshore_settings_form(form_holder5)

        scroll = qtw.QScrollArea()
        scroll.setWidget(form_holder_holder)
        scroll.setMinimumSize(500, 300)
        scroll.setFrameShape(qtw.QFrame.Shape.NoFrame)
        self.layout().addWidget(scroll)

        submit_btn = qtw.QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_forms)
        self.layout().addWidget(submit_btn)

        save_btn = qtw.QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        self.layout().addWidget(save_btn)

        import_btn = qtw.QPushButton("Import")
        import_btn.clicked.connect(self.import_settings)
        self.layout().addWidget(import_btn)

        # entry = qtw.QLineEdit("default")
        # entry.setObjectName("name_field")
        # self.layout().addWidget(entry)
        #
        # combo_box = qtw.QComboBox()
        # combo_box.addItem("Channel A", 0)
        # for i in range(1, 17):
        #     combo_box.addItem(f"Channel {i}", i)
        # self.layout().addWidget(combo_box)
        #
        # spin_box = qtw.QDoubleSpinBox(self)
        # spin_box.setValue(10)
        # spin_box.setRange(0, 100)
        # spin_box.setSingleStep(7.5)
        # spin_box.setSuffix("$")
        # self.layout().addWidget(spin_box)
        #
        # text_box = qtw.QTextEdit(self)
        # text_box.setLineWrapMode(qtw.QTextEdit.LineWrapMode.FixedColumnWidth)
        # text_box.setAcceptRichText(True)
        # text_box.setLineWrapColumnOrWidth(-1)
        # text_box.setPlaceholderText("holder text hello")
        # text_box.setReadOnly(False)
        # text_box.setHtml("<h1><b>Some text!!</b></h1>")
        # self.layout().addWidget(text_box)

        # formLayout is cool

        # b1 = qtw.QPushButton("Click me")
        # b1.clicked.connect(lambda: __clicked__(label, f"{combo_box.currentText()} is {spin_box.value()}\n"
        #                                               f"{text_box.toPlainText()}", text_box))
        # self.layout().addWidget(b1)

        self.show()

    def load_channel_settings_form(self, parent, index=0):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        title = qtw.QLabel("Channel Settings")
        form_layout.addRow(title)

        channel_form = {}
        self.channel_forms.append(channel_form)

        channel = qtw.QComboBox(parent)
        channel.addItem("Channel A", Model372.InputChannel.CONTROL)
        channel.addItem("Channel 1", Model372.InputChannel.ONE)
        channel.addItem("Channel 2", Model372.InputChannel.TWO)
        channel.addItem("Channel 3", Model372.InputChannel.THREE)
        channel.addItem("Channel 4", Model372.InputChannel.FOUR)
        channel.setCurrentIndex(index)
        form_layout.addRow(channel)
        channel_form["channel"] = channel
        channel_form["prev_channel"] = -1

        calibration = qtw.QComboBox(parent)
        for key in TemperatureCalibration.functions.keys():
            calibration.addItem(key, key)
        form_layout.addRow(calibration)
        channel_form["calibration"] = calibration

        excitation_mode = qtw.QComboBox(parent)
        excitation_mode.addItem("current", Model372.SensorExcitationMode.CURRENT)
        excitation_mode.addItem("voltage", Model372.SensorExcitationMode.VOLTAGE)
        form_layout.addRow("Excitation Mode:", excitation_mode)
        channel_form["excitation_mode"] = excitation_mode

        excitation_range = qtw.QComboBox(parent)
        form_layout.addRow("Excitation Range:", excitation_range)
        channel_form["excitation_range"] = excitation_range

        auto_range = qtw.QComboBox(parent)
        auto_range.addItem("On", Model372.AutoRangeMode.CURRENT)
        auto_range.addItem("Off", Model372.AutoRangeMode.OFF)
        form_layout.addRow("Auto Range:", auto_range)
        channel_form["auto_range"] = auto_range

        shunted = qtw.QCheckBox(parent)
        shunted.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
        form_layout.addRow("Shunted:", shunted)
        channel_form["shunted"] = shunted

        units = qtw.QComboBox(parent)
        units.addItem("Ohms", Model372.InputSensorUnits.OHMS)
        units.addItem("Kelvin", Model372.InputSensorUnits.KELVIN)
        form_layout.addRow("Units:", units)
        channel_form["units"] = units

        resistance_range = qtw.QComboBox(parent)
        for x in Model372.MeasurementInputResistance:
            resistance_range.addItem(range_text_converter(x.name), x)
        resistance_range.setCurrentIndex(9)                                 # MeasurementInputResistance.RANGE_63_POINT_2_KIL_OHMS
        form_layout.addRow("Resistance Range:", resistance_range)
        channel_form["resistance_range"] = resistance_range

        channel_form["readings"] = self.load_wanted_readings_checkboxes(form_layout,
                                                                        ["kelvin", "resistance", "power", "quadrature"])

        functionality = qtw.QComboBox(parent)
        functionality.addItem("Basic", "Basic")
        functionality.addItem("Heater", "Heater")
        form_layout.addRow(functionality)
        channel_form["functionality"] = functionality

        channel_form["functionality_form"] = {"old_value": functionality.currentData()}
        for key in FunctionalityFunctions.functions:
            channel_form["functionality_form"][key] = FunctionalityFunctions.functions[key]["load"](parent)
            for item in channel_form["functionality_form"][key].items():
                item[1].setVisible(False)
                form_layout.labelForField(item[1]).setVisible(False)

        def on_channel_changed(value=0):
            quad_boxes = channel_form["readings"][3]
            print(f"old: {channel_form['prev_channel']}, new: {value}")
            if value == 0 and channel_form["prev_channel"] != 0:
                quad_boxes["log"].setEnabled(False)
                quad_boxes["plot"].setEnabled(False)
                quad_boxes["custom_name"].setEnabled(False)
                if excitation_mode.currentIndex() == 0:
                    on_excitation_mode_changed()
                else:
                    excitation_mode.setCurrentIndex(0)
                excitation_mode.setDisabled(True)
                resistance_range.setDisabled(True)
            elif value != 0 and channel_form["prev_channel"] < 1:
                quad_boxes["log"].setEnabled(True)
                quad_boxes["plot"].setEnabled(True)
                quad_boxes["custom_name"].setEnabled(True)
                excitation_mode.setDisabled(False)
                on_excitation_mode_changed()
                resistance_range.setDisabled(False)

            channel_form["prev_channel"] = value

        channel.currentIndexChanged.connect(on_channel_changed)

        def on_excitation_mode_changed(value=0):
            excitation_range.clear()
            print("changed ex mode")
            if value == 0:  # current
                if channel.currentIndex() == 0:
                    for x in Model372.ControlInputCurrentRange:
                        excitation_range.addItem(range_text_converter(x.name), x)
                    excitation_range.setCurrentIndex(1)                     # ControlInputCurrentRange.RANGE_1_NANO_AMP
                else:
                    for x in Model372.MeasurementInputCurrentRange:
                        excitation_range.addItem(range_text_converter(x.name), x)
                    excitation_range.setCurrentIndex(16)                    # MeasurementInputCurrentRange.RANGE_100_MICRO_AMPS
            else:  # voltage TODO: sensible default value
                for x in Model372.MeasurementInputVoltageRange:
                    excitation_range.addItem(range_text_converter(x.name), x)

        excitation_mode.currentIndexChanged.connect(on_excitation_mode_changed)

        def on_functionality_changed():
            print("try change func")
            print(channel_form["functionality_form"])
            func_form = channel_form["functionality_form"]
            old_form = func_form[func_form["old_value"]]
            new_form = func_form[channel_form["functionality"].currentData()]

            for item in old_form.items():
                form_layout.labelForField(item[1]).setVisible(False)
                item[1].setVisible(False)
            print("all destroyed")
            for item in new_form.items():
                form_layout.labelForField(item[1]).setVisible(True)
                item[1].setVisible(True)

            func_form["old_value"] = channel_form["functionality"].currentData()
            parent.parentWidget().setFixedHeight(parent.parentWidget().sizeHint().height())

        functionality.currentIndexChanged.connect(on_functionality_changed)

        # initialize gui elements:
        on_channel_changed(channel.currentIndex())


    def load_wanted_readings_checkboxes(self, form_layout: qtw.QFormLayout, readings: list[str]) -> list[dict]:
        form_layout.addRow(qtw.QLabel("Select Wanted Readings:"))
        rows = []
        for reading in readings:
            line = qtw.QHBoxLayout()
            row = {"reading": reading}

            box_reading = qtw.QCheckBox("log ")
            box_reading.setChecked(True)
            box_reading.setFont(qtg.QFont("Helvetica", 12))
            box_reading.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
            line.addWidget(box_reading)
            row["log"] = box_reading

            box_plot = qtw.QCheckBox("plot ")
            box_plot.setDisabled(not box_reading.isChecked())
            box_plot.setFont(qtg.QFont("Helvetica", 12))
            box_plot.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
            line.addWidget(box_plot)
            row["plot"] = box_plot

            form_layout.addRow(reading, line)

            custom_name = qtw.QLineEdit()
            custom_name.setDisabled(not box_reading.isChecked())
            custom_name.setPlaceholderText(f"{reading}{len(self.channel_forms)}")
            form_layout.addRow(custom_name)
            row["custom_name"] = custom_name

            rows.append(row)

            def on_change(state: bool, box: qtw.QCheckBox, name: qtw.QLineEdit):
                box.setDisabled(not state)
                name.setDisabled((not state))

            box_reading.stateChanged.connect(
                lambda s=box_reading.isChecked(), b=box_plot, n=custom_name: on_change(s, b, n))

        return rows

    def load_lakeshore_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        title = qtw.QLabel("Lakeshore Settings")
        form_layout.addRow(title)

        lakeshore_form = {}

        ip_address = qtw.QLineEdit(parent)
        ip_address.setInputMask("000.000.0.00;_")
        ip_address.setText("192.168.0.12")
        ip_address.setAlignment(Qt.AlignCenter)
        ip_address.setMaximumWidth(190)

        form_layout.addRow("ip: ", ip_address)
        lakeshore_form["ip"] = ip_address

        filter = qtw.QCheckBox(parent)
        filter.setChecked(True)
        form_layout.addRow("use filter: ", filter)
        lakeshore_form["state"] = filter

        settle_time = qtw.QSpinBox(parent)
        settle_time.setRange(1, 200)
        settle_time.setValue(5)
        settle_time.setSuffix("s")
        settle_time.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        settle_time.setAlignment(Qt.AlignRight)
        form_layout.addRow("settle time: ", settle_time)
        lakeshore_form["settle_time"] = settle_time

        window = qtw.QSpinBox(parent)
        window.setRange(1, 80)
        window.setValue(10)
        window.setSuffix("%")
        window.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        window.setAlignment(Qt.AlignRight)
        form_layout.addRow("window: ", window)
        lakeshore_form["window"] = window

        self.lakeshore_form = lakeshore_form




    def load_mpv_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        title = qtw.QLabel("MPV Settings")
        form_layout.addRow(title)

        mpv_form = {}

        mpv_form["readings"] = self.load_wanted_readings_checkboxes(form_layout, ["field", "temperature"])

        self.mpv_form = mpv_form

    def load_logging_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        title = qtw.QLabel("Logging Settings")
        form_layout.addRow(title)

        logging_form = {}

        interval = qtw.QDoubleSpinBox(parent)
        interval.setRange(1, 100)
        interval.setValue(2)
        interval.setSuffix("s")
        interval.setButtonSymbols(qtw.QAbstractSpinBox.ButtonSymbols.NoButtons)
        interval.setAlignment(Qt.AlignRight)
        form_layout.addRow("Interval:", interval)
        logging_form["interval"] = interval

        append_file = qtw.QCheckBox(parent)
        form_layout.addRow("Append Existing File:", append_file)
        logging_form["append"] = append_file

        self.logging_form = logging_form

    def submit_forms(self):
        print("submitting")
        default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "default.csv"))
        print(default_path)

        if GuiHelper.get_data_from_widget(self.logging_form["append"]):
            save_path = qtw.QFileDialog.getOpenFileName(self, "Save", default_path)[0]
            print(save_path)
            self.controller.append_to_file = True
        else:
            save_path = qtw.QFileDialog.getSaveFileName(self, "Save", default_path)[0]
            print(save_path)
            self.controller.append_to_file = False
        self.controller.save_path = save_path

        self.controller.configure_lakeshore(ip=GuiHelper.get_data_from_widget(self.lakeshore_form["ip"]),
                                            state=GuiHelper.get_data_from_widget(self.lakeshore_form["state"]),
                                            settle_time=GuiHelper.get_data_from_widget(self.lakeshore_form["settle_time"]),
                                            window=GuiHelper.get_data_from_widget(self.lakeshore_form["window"]))

        for channel_form in self.channel_forms:
            readings = []
            for reading in channel_form["readings"]:
                if reading["log"].isChecked() and reading["log"].isEnabled():
                    custom_name = reading["custom_name"].text()
                    custom_name = custom_name if len(custom_name) > 0 else reading["custom_name"].placeholderText()
                    readings.append({"reading": reading["reading"],
                                     "plot": reading["plot"].isChecked(),
                                     "custom_name": custom_name})

            channel_settings = ChannelSettings(channel=channel_form["channel"].currentData(),
                                               calibration=channel_form["calibration"].currentData(),
                                               excitation_mode=channel_form["excitation_mode"].currentData(),
                                               excitation_range=channel_form["excitation_range"].currentData(),
                                               auto_range=channel_form["auto_range"].currentData(),
                                               shunted=channel_form["shunted"].isChecked(),
                                               units=channel_form["units"].currentData(),
                                               resistance_range=channel_form["resistance_range"].currentData(),
                                               readings=readings)
            print(channel_settings)
            func = GuiHelper.get_data_from_widget(channel_form["functionality"])
            print(func)
            func_form = channel_form["functionality_form"][func]
            print(func_form)
            functionality_data = FunctionalityFunctions.functions[func]["extract"](func_form)
            print(functionality_data)
            functionality = FunctionalityFunctions.functions[func]["create"](functionality_data)
            print(functionality)

            self.controller.create_channel(channel_settings, functionality)
            # print(channel_settings.create_channel(Device.get_device()))



        mpv_readings = []
        for reading in self.mpv_form["readings"]:
            if reading["log"].isChecked():
                custom_name = reading["custom_name"].text()
                custom_name = custom_name if len(custom_name) > 0 else reading["custom_name"].placeholderText()
                mpv_readings.append({"reading": reading["reading"],
                                     "plot": reading["plot"].isChecked(),
                                     "custom_name": custom_name})

        mpv_settings = MPVSettings(readings=mpv_readings)
        self.controller.create_mpv_wrapper(mpv_settings)

        self.controller.logging_interval = self.logging_form["interval"].value()

        self.controller.ready = True
        self.close()

    def save_settings(self):
        default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "settings", "default.json"))
        print(default_path)
        save_path = qtw.QFileDialog.getSaveFileName(self, "Save", default_path)[0]
        print(save_path)
        if len(save_path) == 0:
            return

        settings = {"channels": [],
                    "mpv": None,
                    "logging": None}

        for channel_form in self.channel_forms:
            readings = []
            for reading in channel_form["readings"]:
                readings.append({"reading": reading["reading"],
                                 "log": reading["log"].isChecked(),
                                 "plot": reading["plot"].isChecked(),
                                 "custom_name": reading["custom_name"].text()})

            func = GuiHelper.get_data_from_widget(channel_form["functionality"])
            func_form = {}
            for item in channel_form["functionality_form"][func].items():
                func_form[item[0]] = GuiHelper.get_save_data_from_widget(item[1])

            settings["channels"].append({"channel": channel_form["channel"].currentIndex(),
                                         "calibration": channel_form["calibration"].currentIndex(),
                                         "excitation_mode": channel_form["excitation_mode"].currentIndex(),
                                         "excitation_range": channel_form["excitation_range"].currentIndex(),
                                         "auto_range": channel_form["auto_range"].currentIndex(),
                                         "shunted": channel_form["shunted"].isChecked(),
                                         "units": channel_form["units"].currentIndex(),
                                         "resistance_range": channel_form["resistance_range"].currentIndex(),
                                         "readings": readings,
                                         "functionality": channel_form["functionality"].currentIndex(),
                                         "functionality_form": func_form})

        mpv_readings = []
        for reading in self.mpv_form["readings"]:
            mpv_readings.append({"reading": reading["reading"],
                                 "log": reading["log"].isChecked(),
                                 "plot": reading["plot"].isChecked(),
                                 "custom_name": reading["custom_name"].text()})

        settings["mpv"] = {"readings": mpv_readings}

        settings["logging"] = {"interval": self.logging_form["interval"].value()}

        with open(save_path, "w") as file:
            s = json.dumps(settings, indent=4)
            file.write(s)

    def import_settings(self):
        print("loading settings")
        default_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "settings", "default.json"))
        print(default_path)
        save_path = qtw.QFileDialog.getOpenFileName(self, "Save", default_path)[0]
        print(save_path)
        if len(save_path) == 0:
            return

        with open(save_path, "r") as file:
            s = "".join(file.readlines())
            settings = json.loads(s)
        for i in range(len(settings["channels"])):
            channel_form = self.channel_forms[i]
            channel_settings = settings["channels"][i]
            channel_form["channel"].setCurrentIndex(channel_settings["channel"])
            channel_form["calibration"].setCurrentIndex(channel_settings["calibration"])
            channel_form["excitation_mode"].setCurrentIndex(channel_settings["excitation_mode"])
            channel_form["excitation_range"].setCurrentIndex(channel_settings["excitation_range"])
            channel_form["auto_range"].setCurrentIndex(channel_settings["auto_range"])
            channel_form["shunted"].setChecked(channel_settings["shunted"])
            channel_form["units"].setCurrentIndex(channel_settings["units"])
            channel_form["resistance_range"].setCurrentIndex(channel_settings["resistance_range"])
            for j in range(len(channel_settings["readings"])):
                reading_settings = channel_settings["readings"][j]
                reading_form = channel_form["readings"][j]
                reading_form["log"].setChecked(reading_settings["log"])
                reading_form["plot"].setChecked(reading_settings["plot"])
                reading_form["custom_name"].setText(reading_settings["custom_name"])
            GuiHelper.change_widget_with_data(channel_form["functionality"], channel_settings["functionality"])
            func_settings = channel_settings["functionality_form"]
            func_form = channel_form["functionality_form"][
                GuiHelper.get_data_from_widget(channel_form["functionality"])]
            for item in func_settings.items():
                GuiHelper.change_widget_with_data(func_form[item[0]], item[1])

        mpv_form = self.mpv_form
        mpv_settings = settings["mpv"]
        for i in range(len(mpv_settings["readings"])):
            reading_settings = mpv_settings["readings"][i]
            reading_form = mpv_form["readings"][i]
            reading_form["log"].setChecked(reading_settings["log"])
            reading_form["plot"].setChecked(reading_settings["plot"])
            reading_form["custom_name"].setText(reading_settings["custom_name"])

        self.logging_form["interval"].setValue(settings["logging"]["interval"])


def show_gui(controller=None):
    app = qtw.QApplication(sys.argv)
    gui = SettingsGui(controller)
    app.exec_()


# just for testing ui
if __name__ == "__main__":
    # t = Thread(target=show_gui())
    show_gui()
