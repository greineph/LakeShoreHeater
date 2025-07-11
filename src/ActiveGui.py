import os
import time
from threading import Thread
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
import sys

from src import GuiHelper
from src.SettingsGui import SettingsGui


class ActiveGui(qtw.QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.paused = False

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
        tabs.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(tabs)

        main_tab = qtw.QWidget()
        self.load_main_tab(main_tab)
        tabs.addTab(main_tab, "Tab 1")

        settings_tab = qtw.QWidget()
        tabs.addTab(settings_tab, "Settings")

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


def show_gui(controller):
    app = qtw.QApplication(sys.argv)
    gui = ActiveGui(controller)
    app.exec_()


# just for testing ui
if __name__ == "__main__":
    show_gui(None)
