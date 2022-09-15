from typing import *
from abc import ABC, abstractmethod
from ..model import Linkage, LinkageTrajectory
from ..view import SplineTargetProvider

import numpy as np

class RetargetingController(ABC):

    @abstractmethod
    def on_trajectory_changed(self):
        pass

    @abstractmethod
    def update_src(self, frame: float, origin: np.ndarray):
        pass

    @abstractmethod
    def update_dest(self, frame: float, origin: np.ndarray):
        pass