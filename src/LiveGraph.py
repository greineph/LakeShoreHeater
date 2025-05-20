import random
from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


# TODO: cant be a thread because matplotlib is weird
class LiveGraph:

    def __init__(self, datahub, x_axis: str, y_axis: list[str]):
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
        plt.ylim(0, 3000)
        plt.xlim(0, 10)
        plt.ion()
        # self.ln, = ax.plot(df[self.x_axis].tolist(),
        #                    df[self.y_axis[0]].tolist())
        self.ln, = ax.plot([1.0, 2.0, 3.0], [1.3, 7.2, 5.8])
        # plt.pause(0.2)
        plt.show(block=False)

    # TODO: update graph in mainloop, add bools for control
    def update(self, data):
        print("updating")
        # df = self.datahub.get_data()
        # x_vals = df[self.x_axis].tolist()
        # y_vals = df[self.y_axis[0]].tolist()
        x_vals = [i for i in range(200)]
        y_vals = [random.randint(0, 2000) for i in range(200)]
        # print(x_vals)
        # print(y_vals)
        self.ln.set_xdata(x_vals)
        self.ln.set_ydata(y_vals)
        plt.xlim(x_vals[0], x_vals[-1])
        # plt.ylim(0, max(y_vals))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
