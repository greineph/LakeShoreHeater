import time
from threading import Thread
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import sys


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

        entry = qtw.QLineEdit("default")
        entry.setObjectName("name_field")
        self.layout().addWidget(entry)

        combo_box = qtw.QComboBox()
        combo_box.addItem("Channel A", 0)
        for i in range(1, 17):
            combo_box.addItem(f"Channel {i}", i)
        self.layout().addWidget(combo_box)

        spin_box = qtw.QDoubleSpinBox(self)
        spin_box.setValue(10)
        spin_box.setRange(0, 100)
        spin_box.setSingleStep(7.5)
        spin_box.setSuffix("$")
        self.layout().addWidget(spin_box)

        text_box = qtw.QTextEdit(self)
        text_box.setLineWrapMode(qtw.QTextEdit.LineWrapMode.FixedColumnWidth)
        text_box.setAcceptRichText(True)
        text_box.setLineWrapColumnOrWidth(-1)
        text_box.setPlaceholderText("holder text hello")
        text_box.setReadOnly(False)
        text_box.setHtml("<h1><b>Some text!!</b></h1>")
        self.layout().addWidget(text_box)

        # formLayout is cool

        b1 = qtw.QPushButton("Click me")
        b1.clicked.connect(lambda: __clicked__(label, f"{combo_box.currentText()} is {spin_box.value()}\n"
                                                      f"{text_box.toPlainText()}", text_box))
        self.layout().addWidget(b1)

        self.show()


def __clicked__(label, text, text_box):
    label.setText(text)
    label.adjustSize()
    text_box.setText("you press?")


def show_gui():
    app = qtw.QApplication(sys.argv)
    gui = Gui()
    app.exec_()


t = Thread(target=show_gui())
