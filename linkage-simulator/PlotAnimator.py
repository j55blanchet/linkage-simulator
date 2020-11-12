"""
Boilerplate for running interactive sketches.

Referenced Code:
- https://stackoverflow.com/questions/11874767/how-do-i-plot-in-real-time-in-a-while-loop-using-matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class PlotAnimator:
    def __init__(self, driver, frames=None):
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

    def run(self, fps: int = 30):

        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames=self.frames,
            init_func=self.setup, 
            blit=True,
            interval=1000 // fps)
        plt.show()

# if __name__ == "__main__":
#     class DummyController:
#         def __init__(self) -> None:
#             self.xdata = []
#             self.ydata = []
#             ln, = plt.plot([], [], 'ro')
#             self.ln = ln

#         def setup(self, sketch: Sketch):
#             sketch.ax.set_xlim(0, 2*np.pi)
#             sketch.ax.set_ylim(-1, 1)
#             return self.ln,

#         def update(self, sketch: Sketch, frame):
#             self.xdata.append(frame)
#             self.ydata.append(np.sin(frame))
#             self.ln.set_data(self.xdata, self.ydata)

#             # sketch.fig.gca().relim()
#             # sketch.fig.gca().autoscale_view()
#             return self.ln,

#     Sketch(DummyController()).run()
# ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=100)
# plt.show()

# class PlotAnimator:

#     FPS = 30

#     def __init__(self, controller):
        
#         self.controller = controller

#         self.ani = None
#         fig, ax = plt.subplots()
#         self.fig = fig
#         self.ax = ax
        
#         self.pmouseX, self.pmouseY = -1, -1
#         self.mouseX, self.mouseY = -1, -1

#     def run(self):

#         connections = [
#             plt.connect('motion_notify_event', self.on_mouse_move)
#         ]
        
#         self.ani = FuncAnimation(self.fig, self.update, init_func=self.setup, blit=True, interval= 1 / PlotAnimator.FPS)
#         plt.show()

#         for c in connections:
#             plt.disconnect(c)

#     def setup(self):
#         return self.controller.setup(self)

#     def update(self, frame):
#         self.pmouseX = self.mouseX
#         self.pmouseY = self.mouseY
#         self.controller.update(self)

#     def on_mouse_move(self, event):
#         self.mouseX = event.x
#         self.mouseY = event.y

# if __name__ == "__main__":
#     class DummyController:
#         def __init__(self) -> None:
#             self.ln = plt.plot([], [])
#             pass
#         def update(self, anim):
#             print((anim.mouseX, anim.mouseY))

#         def setup(self, anim):
#             return self.ln,

#     anim = PlotAnimator(DummyController())
#     anim.run()








# from matplotlib import pyplot
# from matplotlib.animation import FuncAnimation
# from .Linkage import Linkage
# import noise
# import random

# # class LinkageSimulator:



# #     def update(self, frame):
        

# #     pass

# x_data, y_data = [], []

# figure = pyplot.figure()
# line, _ = pyplot.plot(x_data, y_data, '-')

# x = 0

# def update(frame):
#     global x
#     x_data.append(x)
#     x += 1
#     y_data.append(noise.pnoise1(x))
#     line.set_data(x_data, y_data)
#     figure.gca().relim()
#     figure.gca().autoscale_view()
#     return line,
    

# animation = FuncAnimation(figure, update, interval=200)

# pyplot.show()




