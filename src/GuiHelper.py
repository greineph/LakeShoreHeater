from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt

# this file aims to provide useful functions when handling pyqt stuff

# TODO: finish
def get_data_from_widget(widget: qtw.QWidget):
    match type(widget):
        case qtw.QComboBox:
            return widget.currentData()
        case qtw.QCheckBox:
            return widget.isChecked()
        case qtw.QLineEdit:
            return widget.text()
        case qtw.QSpinBox | qtw.QDoubleSpinBox:
            return widget.value()
        case _:
            return None