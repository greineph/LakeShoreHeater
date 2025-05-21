import random
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class LiveGraph:

    # TODO: maybe reference DataFrame instead of datahub for data gathering,
    #       FuncAnimation might actually work better idk yet
    def __init__(self, datahub, x_axis: str, y_axis: list[str]):
        super().__init__()
        self.datahub = datahub
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fig = None
        self.ln = None
        self.lines: list[plt.Line2D] = []

    # TODO: initialize plot style and labels and stuff
    #       put this in init probably
    def initialize(self):
        df = self.datahub.get_data()
        style.use("seaborn-v0_8-whitegrid")
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        plt.ylim(0, 400)
        plt.xlim(0, 10)
        plt.ion()
        for y in self.y_axis:
            ln, = ax.plot([], [])
            self.lines.append(ln)
        ax.legend(self.y_axis)
        plt.tight_layout()
        plt.pause(0.2)

    # TODO: update graph in mainloop, add bools for control
    def update(self):
        df = self.datahub.get_data()
        if len(df) < 1:
            return

        x_vals = df[self.x_axis].tolist()
        val_len = len(x_vals)
        for i in range(len(self.y_axis)):
            y_vals = df[self.y_axis[i]].tolist()[:val_len]
            self.lines[i].set_xdata(x_vals)
            self.lines[i].set_ydata(y_vals)
        plt.xlim(x_vals[0], max(10, x_vals[-1]))
        # plt.ylim(0, max(y_vals))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
