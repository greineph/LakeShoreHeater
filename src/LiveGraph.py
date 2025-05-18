from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

from src.Datahub import Datahub


# TODO: possibly doesn't need to be a Thread
class LiveGraph(Thread):

    def __init__(self, datahub: Datahub, x_axis: str, y_axis: list[str]):
        super().__init__()
        self.datahub = datahub
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fig = None
        self.ln = None

    # TODO: initialize plot style and labels and stuff
    def run(self):
        df = self.datahub.get_data()
        style.use("seaborn-v0_8-whitegrid")
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        plt.ylim(0, 400)
        self.ln, = ax.plot(df[self.x_axis].tolist(),
                           [df[y].tolist() for y in self.y_axis])

    # TODO: figure out how to update the graph (is matplotlib animation necessary?)
    def update(self, data):
        df = self.datahub.get_data()
        x_vals = df[self.x_axis].tolist()
        y_vals = [df[y] for y in self.y_axis]
        self.ln.set_xdata(x_vals)
        self.ln.set_ydata(y_vals)
        plt.xlim(x_vals[0], x_vals[-1])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
