from abc import ABC, abstractmethod
from typing import Tuple



class Linkage(ABC):
    Bounds = Tuple[float, float, float, float]

    @abstractmethod
    def get_plot_bounds(self) -> Bounds:
        raise NotImplemented()
    
    @abstractmethod
    def draw(self, ax, prev):
        raise NotImplemented()