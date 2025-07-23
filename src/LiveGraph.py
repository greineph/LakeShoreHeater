import random
import time

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
        self.running = True

    def run(self):
        print("start")
        self.initialize()
        while self.running:
            self.check_queue()
            self.update()

    def initialize(self):
        style.use("seaborn-v0_8-whitegrid")
        self.fig = plt.figure()
        self.fig.canvas.mpl_connect("close_event", self.on_close)
        ax = self.fig.add_subplot(111)
        plt.ylim(-10, 500)
        plt.xlim(0, 10)
        plt.ion()
        for y in self.y_axis:
            ln, = ax.plot([], [])
            self.lines.append(ln)
        ax.legend(self.y_axis)
        plt.tight_layout()
        plt.pause(0.1)

    def on_close(self, event):
        self.running = False

    def check_queue(self):
        while not self.queue.empty():
            self.add_data(self.queue.get())

    def add_data(self, data):
        self.df.loc[len(self.df)] = data

    def update(self):
        if self.df.empty:
            return

        x_vals = self.df[self.x_axis].tolist()
        val_len = len(x_vals)
        for i in range(len(self.y_axis)):
            y_vals = self.df[self.y_axis[i]].tolist()[:val_len]
            self.lines[i].set_xdata(x_vals)
            self.lines[i].set_ydata(y_vals)
        plt.xlim(x_vals[0], max(10, x_vals[-1]))
        # plt.ylim(0, max(y_vals))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
