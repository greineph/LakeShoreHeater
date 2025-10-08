import os
import sys

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt


class TemperatureCalibrationGui(qtw.QWidget):

    def __init__(self):
        super().__init__()
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

        form = {}

        name = qtw.QLineEdit()
        form_layout.addRow("Name:", name)
        form["name"] = name

        min_input = qtw.QLineEdit()
        form_layout.addRow("Minimum Input:", min_input)
        form["min_input"] = min_input

        max_input = qtw.QLineEdit()
        form_layout.addRow("Maximum Input:", max_input)
        form["max_input"] = max_input

        rescale_0 = qtw.QLineEdit()
        form_layout.addRow("Rescale 0:", rescale_0)
        form["rescale_0"] = rescale_0

        rescale_1 = qtw.QLineEdit()
        form_layout.addRow("Rescale 1:", rescale_1)
        form["rescale_1"] = rescale_1

        func_params = qtw.QTextEdit()
        form_layout.addRow("Function Parameters", func_params)
        form["func_params"] = func_params

        min_output = qtw.QLineEdit()
        form_layout.addRow("Minimum Output:", min_output)
        form["min_output"] = min_output

        max_output = qtw.QLineEdit()
        form_layout.addRow("Maximum Output:", max_output)
        form["max_output"] = max_output

        create_btn = qtw.QPushButton("Create")
        create_btn.clicked.connect(lambda: print("created"))
        self.layout().addWidget(create_btn)

        self.show()


# just for testing ui
if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    gui = TemperatureCalibrationGui()
    app.exec_()
