from threading import Thread
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


class LiveGraph(Thread):

    def __init__(self, ):
        super().__init__()

    def run(self):
        style.use("seaborn-v0_8-whitegrid")
        plt.show()

    # TODO: figure out how to update the graph (is matplotlib animation necessary?)
    def update(self, data):
        data.plot(x="c1", y=["c2"])

