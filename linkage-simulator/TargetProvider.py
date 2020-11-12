from abc import ABC, abstractmethod

from matplotlib.lines import Line2D

from .linkage_types import *

class TargetProvider(ABC):
    
    @property
    @abstractmethod
    def target(self) -> Point2d:
        return 0, 0
    
    @abstractmethod
    def update_target(self, tt: float, dt: float):
        pass

    def draw(self, ax, line: Line2D = None):
        x, y = self.target

        if line is None:
            return ax.plot([x], [y],  "ro", label="Target", marker='x')[0]
        
        line.set_data([x], [y])
        return line

    def button_clicked(self, mouse_x: float, mouse_y: float):
        pass

    @staticmethod
    def interpolate(p1: Point2d, p2: Point2d, t: float) -> Point2d:
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        return x1 + dx * t, y1 + dy * t