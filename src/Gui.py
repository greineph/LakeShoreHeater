import time
from threading import Thread
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt
import sys
from InputData import range_text_converter
from Channel import ChannelSettings
from MPVWrapper import MPVSettings

from UliEngineering.Electronics.Resistors import resistor_tolerance
from lakeshore import Model372

from src.Device import Device


# TODO: gui has to be in a thread because matplotlib has to be in the mainthread :>
#   maybe make gui main thread and put graph/ datahub in process or this in process idk
#   or if possible implement matplot graph into ui so everything works ._.
class Gui(qtw.QWidget):

    def __init__(self, controller=None):
        super().__init__()

        self.controller = controller

        self.channel_forms = []
        self.mpv_form = {}

        # self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Setup")

        self.setLayout(qtw.QVBoxLayout())

        self.setFont(qtg.QFont("Helvetica", 16))

        label = qtw.QLabel("Settings")
        title_font = qtg.QFont("Helvetica", 30)
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

        submit_btn = qtw.QPushButton("Submit")
        submit_btn.clicked.connect(self.submit_forms)
        self.layout().addWidget(submit_btn)

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

        title = qtw.QLabel("Lakeshore Settings")
        form_layout.addRow(title)

        channel_form = {}

        channel = qtw.QComboBox(parent)
        channel.addItem("Channel A", Model372.InputChannel.CONTROL)
        channel.addItem("Channel 1", Model372.InputChannel.ONE)
        channel.addItem("Channel 2", Model372.InputChannel.TWO)
        channel.addItem("Channel 3", Model372.InputChannel.THREE)
        channel.addItem("Channel 4", Model372.InputChannel.FOUR)
        channel.setCurrentIndex(index)
        form_layout.addRow(channel)
        channel_form["channel"] = channel

        excitation_mode = qtw.QComboBox(parent)
        excitation_mode.addItem("current", Model372.SensorExcitationMode.CURRENT)
        excitation_mode.addItem("voltage", Model372.SensorExcitationMode.VOLTAGE)
        form_layout.addRow("Excitation Mode:", excitation_mode)
        channel_form["excitation_mode"] = excitation_mode

        excitation_range = qtw.QComboBox(parent)
        for x in Model372.MeasurementInputCurrentRange:
            excitation_range.addItem(range_text_converter(x.name), x)
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
        form_layout.addRow("Resistance Range:", resistance_range)
        channel_form["resistance_range"] = resistance_range

        channel_form["readings"] = self.load_wanted_readings_checkboxes(form_layout,
                                                                        ["kelvin", "resistance", "power", "quadrature"])

        self.channel_forms.append(channel_form)

        # TODO: possibly change selectable ranges if channel is Control or not
        def on_channel_changed(value=0):
            print(value)

        channel.currentIndexChanged.connect(on_channel_changed)

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

    def load_mpv_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        title = qtw.QLabel("MPV Settings")
        form_layout.addRow(title)

        mpv_form = {}

        mpv_form["readings"] = self.load_wanted_readings_checkboxes(form_layout, ["field", "temperature"])

        self.mpv_form = mpv_form

    def submit_forms(self):
        print("submitting")
        for channel_form in self.channel_forms:
            readings = []
            for reading in channel_form["readings"]:
                if reading["log"].isChecked():
                    custom_name = reading["custom_name"].text()
                    custom_name = custom_name if len(custom_name) > 0 else reading["custom_name"].placeholderText()
                    readings.append({"reading": reading["reading"],
                                     "plot": reading["plot"].isChecked(),
                                     "custom_name": custom_name})

            channel_settings = ChannelSettings(channel=channel_form["channel"].currentData(),
                                               excitation_mode=channel_form["excitation_mode"].currentData(),
                                               excitation_range=channel_form["excitation_range"].currentData(),
                                               auto_range=channel_form["auto_range"].currentData(),
                                               shunted=channel_form["shunted"].isChecked(),
                                               units=channel_form["units"].currentData(),
                                               resistance_range=channel_form["resistance_range"].currentData(),
                                               readings=readings)
            print(channel_settings)
            self.controller.create_channel(channel_settings)
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

        self.close()


def __clicked__(label, text, text_box):
    label.setText(text)
    label.adjustSize()
    text_box.setText("you press?")


def show_gui(controller=None):
    app = qtw.QApplication(sys.argv)
    gui = Gui(controller)
    app.exec_()


# just for testing ui
if __name__ == "__main__":
    # t = Thread(target=show_gui())
    show_gui()
