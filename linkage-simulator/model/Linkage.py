from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Sequence, Tuple, Union

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

@dataclass
class LinkageTrajectory:
    stateDuration: float = 1 / 30.0
    states: List[Any] = field(default_factory=list)
    
    def clear_states(self):
        self.states = []