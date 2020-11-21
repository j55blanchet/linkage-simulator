from abc import ABC, abstractmethod, abstractproperty
from typing import Union

import numpy as np

from ..model import *

class LinkageController(ABC):

    @abstractmethod
    def update(self, linkage: Linkage, target: np.array):
        pass

    @abstractmethod
    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        pass