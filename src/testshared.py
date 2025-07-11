import multiprocessing
import threading
import time
import multiprocessing as mp

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import random
import pandas as pd
import tkinter as tk
import ActiveGui


class Graph(mp.Process):

    def __init__(self, queue: mp.Queue):
        super().__init__()
        self.change_limits = None
        self.ln = None
        self.ax = None
        self.fig = None
        self.df = None
        self.queue = queue

    def run(self):
        print(self.queue)
        self.initialize()
        while True:
            self.update()
            self.check_queue()

    def initialize(self):
        style.use("seaborn-v0_8-whitegrid")
        self.df = pd.DataFrame({"c1": [i for i in range(5)],
                                "c2": [random.uniform(0, 90) for i in range(5)]})
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        plt.ion()
        self.ln, = self.ax.plot(self.df["c1"], self.df["c2"])
        plt.ylim(0, 100)
        plt.pause(0.1)
        self.change_limits = True

    def new_data(self, data):
        print(f"received new data {data}")
        self.df.loc[len(self.df)] = [len(self.df), data]

    def check_queue(self):
        while not self.queue.empty():
            self.new_data(self.queue.get())

    def update(self):
        # print(f"updating {self.df}")
        x_vals = self.df["c1"].tolist()
        y_vals = self.df["c2"].tolist()
        self.ln.set_xdata(x_vals)
        self.ln.set_ydata(y_vals)
        if self.change_limits:
            plt.xlim(x_vals[0], x_vals[-1])
            plt.ylim(0, 100)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class Reader(threading.Thread):

    def __init__(self, queue: mp.Queue):
        super().__init__()
        self.queue = queue
        self.last = 45.0

    def run(self):
        print("thread started")
        while True:
            self.last = min(90.0, max(0.0, self.last + random.uniform(-2, 2)))
            self.queue.put(self.last)
            print("new reading")
            # print("hi Im a thread")
            time.sleep(0.1)


class Gui(threading.Thread):

    def __init__(self, graph):
        super().__init__()
        self.root = None
        self.graph = graph
        # self.root.geometry("800x500")
        # self.root.title("Testing")
        # base_font = ('Arial', 16)
        # title_font = ('Arial', 30)

    def run(self):
        self.root = tk.Tk()
        self.root.geometry("800x500")
        self.root.title("Testing")
        tk.Button(self.root, text="On", font=('Arial', 16), pady=0, bg="lightgreen", command=self.start_limits).pack()
        tk.Button(self.root, text="Off", font=('Arial', 16), pady=0, bg="lightgreen", command=self.stop_limits).pack()
        self.root.mainloop()

    def stop_limits(self):
        self.graph.change_limits = False

    def start_limits(self):
        self.graph.change_limits = True


if __name__ == "__main__":
    queue = mp.Queue()
    g = Graph(queue)
    g.daemon = True
    g.start()
    r = Reader(queue)
    r.start()
    # ActiveGui.show_gui()
    print("gui started")
    while True:
        time.sleep(1)



