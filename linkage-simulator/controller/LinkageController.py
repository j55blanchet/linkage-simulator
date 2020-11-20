from abc import ABC, abstractmethod, abstractproperty
from typing import Union

import numpy as np

from ..model import *

LinkageModel = Union[LinkageNetwork, Linkage]

class LinkageController(ABC):

    @abstractmethod
    def update(self, linkage: LinkageModel, target: np.array):
        pass

    @abstractmethod
    def meets_target(self, linkage: LinkageModel, target: np.array) -> bool:
        pass