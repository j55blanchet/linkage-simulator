from abc import ABC, abstractmethod, abstractproperty

from .linkage_types import *
from .Linkage import Linkage

class LinkageController(ABC):

    @abstractmethod
    def update(self, linkage: Linkage, target: Point2d):
        pass

    @abstractmethod
    def meets_target(self, linkage: Linkage, target: Point2d) -> bool:
        pass
