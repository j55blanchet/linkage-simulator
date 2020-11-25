from abc import ABC, abstractmethod
from typing import Sequence, Tuple, Union

import matplotlib.axes
import matplotlib.artist

class Linkage(ABC):
    Bounds = Tuple[float, float, float, float]

    @abstractmethod
    def get_plot_bounds(self) -> Bounds:
        raise NotImplemented()
    
    @abstractmethod
    def draw(self, 
             ax: matplotlib.axes.Axes, 
             prev: Union[Sequence[matplotlib.artist.Artist], None]) \
                -> Sequence[matplotlib.artist.Artist]:

        raise NotImplemented()