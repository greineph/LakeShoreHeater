import random
import time
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from matplotlib import style
from multiprocessing import Process, Queue


class LiveGraph(Process):

    def __init__(self, queue: Queue, df: pd.DataFrame, x_axis: str, y_axis: list[str]):
        super().__init__()
        self.queue = queue
        self.df = df
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fig = None
        self.lines: list[plt.Line2D] = []
        self.running = False

        self.auto_xlim = True
        self.auto_ylim = False
        self.ylim_values = [0.1, 500]

        self.timestamp = time.monotonic()

    def run(self):
        print("start")
        self.initialize()
        self.running = True
        while self.running:
            self.check_queue()
            self.update()

    def initialize(self):
        style.use("seaborn-v0_8-whitegrid")
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("close_event", self.on_close)
        ax = self.fig.add_subplot(111)
        plt.yscale("log")
        plt.ylim(0.1, 500)
        plt.xlim(0, 10)
        plt.ion()
        for y in self.y_axis:
            ln, = ax.plot([], [])
            self.lines.append(ln)
        ax.legend(self.y_axis, loc="upper right")
        plt.tight_layout()
        plt.pause(0.1)

    def on_close(self, event):
        self.running = False

    def check_queue(self):
        while not self.queue.empty():
            item = self.queue.get()
            match item[0]:
                case "data":
                    self.add_data(item[1])
                case "op":
                    self.execute_operation(item[1])
                case _:
                    pass

    def add_data(self, data):
        self.df.loc[len(self.df)] = data

    def execute_operation(self, op):
        match op:
            case Operations.ENABLE_XLIM:
                self.auto_xlim = True
            case Operations.DISABLE_XLIM:
                self.auto_xlim = False
            case Operations.ENABLE_YLIM:
                self.auto_ylim = True
            case Operations.ENABLE_YLIM:
                self.auto_ylim = False
            case _:
                pass

    def update(self):
        if self.df.empty:
            return

        x_vals = self.df[self.x_axis].tolist()
        val_len = len(x_vals)
        for i in range(len(self.y_axis)):
            y_vals = self.df[self.y_axis[i]].tolist()[:val_len]
            self.lines[i].set_xdata(x_vals)
            self.lines[i].set_ydata(y_vals)
            if y_vals[-1] < self.ylim_values[0]:
                self.ylim_values[0] = y_vals[-1]
            if y_vals[-1] > self.ylim_values[1]:
                self.ylim_values[1] = y_vals[-1]

        if self.auto_xlim:
            plt.xlim(x_vals[0], max(10, x_vals[-1]))
        if self.auto_ylim:
            plt.ylim(self.ylim_values[0] * 0.9, self.ylim_values[1] * 1.1)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        # used for performance testing
        temp = time.monotonic()
        print(f"time: {temp - self.timestamp}\nfps: {(temp - self.timestamp) ** -1}")
        self.timestamp = temp


class Operations(Enum):
    ENABLE_XLIM = 0
    DISABLE_XLIM = 1
    ENABLE_YLIM = 2
    DISABLE_YLIM = 3
