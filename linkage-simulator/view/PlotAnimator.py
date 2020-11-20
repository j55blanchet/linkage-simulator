"""
Boilerplate for running interactive sketches.

Referenced Code:
- https://stackoverflow.com/questions/11874767/how-do-i-plot-in-real-time-in-a-while-loop-using-matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

LinkageDriver = "LinkageDriver"

class PlotAnimator:
    def __init__(self, driver: LinkageDriver, frames=None):
        self.driver = driver
        self.frames = frames

        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
    
    def setup(self):
        x_min, x_max, y_min, y_max = self.driver.get_plot_size()

        self.ax.set_xlim(x_min, x_max) 
        self.ax.set_ylim(y_min, y_max)

        return self.driver.plot(self.ax)

    def update(self, frame):
        self.driver.update(frame)
        return self.driver.plot(self.ax)

    def on_mouse_move(self, e):
        print(e)

    def on_mouse_click(self, e):
        if e.xdata != None and e.ydata != None:
            self.driver.button_clicked(e.xdata, e.ydata)

    def run(self, fps: int = 30, save_res: bool = False):

        connections = {
            # 'motion_notify_event': self.on_mouse_move,
            'button_press_event': self.on_mouse_click
        }

        cids = [
            self.fig.canvas.mpl_connect(key, connections[key])
            for key in connections
        ]

        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames=self.frames,
            init_func=self.setup, 
            blit=True,
            interval=1000 // fps)
        plt.show()

        for cid in cids:
            self.fig.canvas.mpl_disconnect(cid)

        if save_res:
            ani.save("output.mp4")