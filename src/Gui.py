import time
from threading import Thread
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import sys
from InputData import range_text_converter

from UliEngineering.Electronics.Resistors import resistor_tolerance
from lakeshore import Model372


# TODO: gui has to be in a thread because matplotlib has to be in the mainthread :>
#   maybe make gui main thread and put graph/ datahub in process or this in process idk
#   or if possible implement matplot graph into ui so everything works ._.
class Gui(qtw.QWidget):

    def __init__(self):
        super().__init__()

        # self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("Setup")

        self.setLayout(qtw.QVBoxLayout())

        self.setFont(qtg.QFont("Helvetica", 16))

        label = qtw.QLabel("label testering")
        label.setFont(qtg.QFont("Helvetica", 30))
        self.layout().addWidget(label)

        form_holder_holder = qtw.QWidget()
        form_holder_holder.setLayout(qtw.QHBoxLayout())
        self.layout().addWidget(form_holder_holder)

        form_holder = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder)
        self.load_channel_settings_form(form_holder)

        form_holder2 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder2)
        self.load_channel_settings_form(form_holder2)

        form_holder3 = qtw.QWidget()
        form_holder_holder.layout().addWidget(form_holder3)
        self.load_mvp_settings_form(form_holder3)

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

    def load_channel_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        channel = qtw.QComboBox(parent)
        channel.addItem("Channel A", 0)
        for i in range(1, 5):
            channel.addItem(f"Channel {i}", i)
        form_layout.addRow(channel)

        excitation_mode = qtw.QComboBox(parent)
        excitation_mode.addItem("current", Model372.SensorExcitationMode.CURRENT)
        excitation_mode.addItem("voltage", Model372.SensorExcitationMode.VOLTAGE)
        form_layout.addRow("Excitation Mode:", excitation_mode)

        excitation_range = qtw.QComboBox(parent)
        for x in Model372.MeasurementInputCurrentRange:
            excitation_range.addItem(range_text_converter(x.name), x)
        form_layout.addRow("Excitation Range:", excitation_range)

        auto_range = qtw.QComboBox(parent)
        auto_range.addItem("On", Model372.AutoRangeMode.CURRENT)
        auto_range.addItem("Off", Model372.AutoRangeMode.OFF)
        form_layout.addRow("Auto Range:", auto_range)

        shunted = qtw.QCheckBox(parent)
        shunted.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
        form_layout.addRow("Shunted:", shunted)

        units = qtw.QComboBox(parent)
        units.addItem("Ohms", Model372.InputSensorUnits.OHMS)
        units.addItem("Kelvin", Model372.InputSensorUnits.KELVIN)
        form_layout.addRow("Units:", units)

        resistance_range = qtw.QComboBox(parent)
        for x in Model372.MeasurementInputResistance:
            resistance_range.addItem(range_text_converter(x.name), x)
        form_layout.addRow("Resistance Range:", resistance_range)

        self.load_wanted_readings_checkboxes(form_layout, ["kelvin", "resistance", "power", "quadrature"])


        def on_channel_changed(value=0):
            print(value)

        channel.currentIndexChanged.connect(on_channel_changed)

    def load_wanted_readings_checkboxes(self, form_layout: qtw.QFormLayout, readings: list[str]):
        form_layout.addRow(qtw.QLabel("Select Wanted Readings:"))
        for reading in readings:
            line = qtw.QHBoxLayout()

            box_reading = qtw.QCheckBox("read ")
            box_reading.setChecked(True)
            box_reading.setFont(qtg.QFont("Helvetica", 12))
            box_reading.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
            line.addWidget(box_reading)

            box_plot = qtw.QCheckBox("plot ")
            box_plot.setDisabled(not box_reading.isChecked())
            box_plot.setFont(qtg.QFont("Helvetica", 12))
            box_plot.setStyleSheet("QCheckBox::indicator { width:20px; height: 20px;}")
            line.addWidget(box_plot)

            def on_change(state: bool, box: qtw.QCheckBox):
                box.setDisabled(not state)

            box_reading.stateChanged.connect(lambda s=box_reading.isChecked(), b=box_plot: on_change(s, b))

            form_layout.addRow(reading, line)

    def load_mvp_settings_form(self, parent):
        form_layout = qtw.QFormLayout()
        parent.setLayout(form_layout)

        self.load_wanted_readings_checkboxes(form_layout, ["field", "temperature"])




def __clicked__(label, text, text_box):
    label.setText(text)
    label.adjustSize()
    text_box.setText("you press?")


def show_gui():
    app = qtw.QApplication(sys.argv)
    gui = Gui()
    app.exec_()


t = Thread(target=show_gui())
