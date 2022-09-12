from typing import *
from abc import ABC, abstractmethod
from ..model import Linkage, LinkageTrajectory
from ..view import SplineTargetProvider

class RetargeterBase(ABC):

    @abstractmethod
    def retarget(
        srcModel: Linkage,
        srcTrajectory: LinkageTrajectory,
        destModel: Linkage,
    ) -> LinkageTrajectory:
    
        raise NotImplementedError()