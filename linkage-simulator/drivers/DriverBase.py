
from abc import ABC, abstractmethod
from typing import *

from matplotlib.lines import Line2D


class DriverBase(ABC):
    
    @abstractmethod
    def get_plot_size(self) -> Tuple[float, float, float, float]:
        pass

    @abstractmethod
    def update(self, frame: float, t: float):
        pass

    @abstractmethod
    def plot(self, ax) -> Tuple[Line2D]:
        pass
    
    def mouse_pressed(self, x, y, e):
        pass

    def mouse_moved(self, x, y, e):
        pass

    def mouse_released(self, x, y, e):
        pass