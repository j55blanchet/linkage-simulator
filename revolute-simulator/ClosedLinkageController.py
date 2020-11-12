
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .Linkage import Linkage
from typing import Tuple
import random
from .PlotAnimator import PlotAnimator

class LinkageDriver:
    def __init__(self, linkage: Linkage) -> None:
        self.linkage = linkage
        self.ln = None

    def get_plot_size(self) -> Tuple[float, float, float, float]:

        buffer_percent = 0.10
        link_maxlen = sum(self.linkage.links)

        size = (1 + buffer_percent) * link_maxlen
        return (-size, size, -size, size)


    def update(self, frame: float):
        spd = 0.01
        for i in range(len(self.linkage.angles)):
            self.linkage.angles[i] += spd * (-0.5 + random.random())
        pass

    def plot(self, ax) -> Tuple[Line2D]:
        self.ln = self.linkage.draw(ax, self.ln)
        return self.ln,


if __name__ == "__main__":
    linkage = Linkage([2, 1])
    driver = LinkageDriver(linkage)
    anim = PlotAnimator(driver)
    anim.run()