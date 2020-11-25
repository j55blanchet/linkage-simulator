from abc import ABC, abstractmethod, abstractproperty
from typing import List

import numpy as np
import matplotlib.artist

from ..model import *

class LinkageController(ABC):

    @abstractmethod
    def update(self, linkage: Linkage, target: np.array):
        pass

    @abstractmethod
    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        pass

    def draw(self) -> List[matplotlib.artist.Artist]:
        return []