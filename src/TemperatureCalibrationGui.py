import json
import os
import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt

from src import GuiHelper


class TemperatureCalibrationGui(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.form = {}

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle("  Temperature Calibration")
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "icon.png"))
        self.setWindowIcon(qtg.QIcon(path))

        self.setLayout(qtw.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.setFont(qtg.QFont("Bahnschrift", 16))
        self.setStyleSheet(" QToolTip{ font: 16pt }")
        self.setToolTipDuration(0)

        title = qtw.QLabel("Settings")
        title_font = qtg.QFont("Bahnschrift", 30)
        # title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(title)

        form_holder = qtw.QWidget()
        form_layout = qtw.QFormLayout()
        form_layout.setSpacing(10)
        form_holder.setLayout(form_layout)
        self.layout().addWidget(form_holder)

        name = qtw.QLineEdit()
        form_layout.addRow("Name", name)
        self.form["name"] = name

        min_resistance = qtw.QLineEdit()
        form_layout.addRow("Minimum Resistance", min_resistance)
        self.form["min_resistance"] = min_resistance

        max_resistance = qtw.QLineEdit()
        form_layout.addRow("Maximum Resitance", max_resistance)
        self.form["max_resistance"] = max_resistance

        rescale_0 = qtw.QLineEdit()
        rescale_0.setText("11.2")
        rescale_0.setPlaceholderText("11.2")
        form_layout.addRow("Rescale 0", rescale_0)
        self.form["rescale_0"] = rescale_0

        rescale_1 = qtw.QLineEdit()
        rescale_1.setText("1400")
        rescale_1.setPlaceholderText("1400")
        form_layout.addRow("Rescale 1", rescale_1)
        self.form["rescale_1"] = rescale_1

        func_params = qtw.QTextEdit()
        form_layout.addRow("Function Parameters", func_params)
        self.form["func_params"] = func_params

        min_temperature = qtw.QLineEdit()
        form_layout.addRow("Minimum Temperature", min_temperature)
        self.form["min_temperature"] = min_temperature

        max_temperature = qtw.QLineEdit()
        form_layout.addRow("Maximum Temperature", max_temperature)
        self.form["max_temperature"] = max_temperature

        create_btn = qtw.QPushButton("Create")
        create_btn.clicked.connect(self.create_file)
        self.layout().addWidget(create_btn)

        self.show()

    def create_file(self):
        name = GuiHelper.get_data_from_widget(self.form["name"])
        min_resistance = GuiHelper.get_data_from_widget(self.form["min_resistance"])
        print(min_resistance)
        min_resistance = float(min_resistance)
        max_resistance = GuiHelper.get_data_from_widget(self.form["max_resistance"])
        print(max_resistance)
        max_resistance = float(max_resistance)
        rescale_0 = GuiHelper.get_data_from_widget(self.form["rescale_0"])
        print(rescale_0)
        rescale_0 = float(rescale_0)
        rescale_1 = GuiHelper.get_data_from_widget(self.form["rescale_1"])
        print(rescale_1)
        rescale_1 = float(rescale_1)
        func_params = GuiHelper.get_data_from_widget(self.form["func_params"])
        print(func_params)
        func_params = [float(l) for l in func_params.split("\n")]
        min_temperature = GuiHelper.get_data_from_widget(self.form["min_temperature"])
        min_temperature = float(min_temperature)
        max_temperature = GuiHelper.get_data_from_widget(self.form["max_temperature"])
        max_temperature = float(max_temperature)

        values = {
            "name": name,
            "min_resistance": min_resistance,
            "max_resistance": max_resistance,
            "rescale_0": rescale_0,
            "rescale_1": rescale_1,
            "func_params": func_params,
            "min_temperature": min_temperature,
            "max_temperature": max_temperature
        }
        print(values)

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "calibrations", str(name) + ".json"))
        with open(path, "w") as file:
            s = json.dumps(values, indent=4)
            file.write(s)


# just for testing ui
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    gui = TemperatureCalibrationGui()
    app.exec_()
