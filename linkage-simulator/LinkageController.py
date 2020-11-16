from abc import ABC, abstractmethod, abstractproperty

import numpy as np

from .linkage_types import *
from .Linkage import Linkage

class LinkageController(ABC):

    @abstractmethod
    def update(self, linkage: Linkage, target: np.array):
        pass

    @abstractmethod
    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        pass
