from ..model import OpenLinkage
from ..view import SplineTargetProvider
from ..controller import DifferentialKinematicOpenLinkageController
from .RetargetingController import RetargetingController

import numpy as np

class DiffKinematicsRetargetingController(RetargetingController):
    
    def __init__(self, 
        src_model: OpenLinkage, 
        dest_model: OpenLinkage, 
        target_provider: SplineTargetProvider
    ):
        self.src_model = src_model
        self.dest_model = dest_model
        self.target_provider = target_provider
        self.controller = DifferentialKinematicOpenLinkageController()

    def on_trajectory_changed(self):
        # noop - kinematics are computed each frame.
        pass

    def update_dest(self, frame: float, origin: np.ndarray):
        if self.target_provider.spline_fn is not None:
            self.controller.update(self.dest_model, self.target_provider.target - origin, iterations=4, max_movement=1.0)

    def update_src(self, frame: float, origin: np.ndarray):
        if self.target_provider.spline_fn is not None:
            self.controller.update(self.src_model, self.target_provider.target - origin, iterations=4, max_movement=1.0)
            
            
        
        