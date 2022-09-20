from ..model import OpenLinkage
from ..view import SplineTargetProvider
from ..controller import LinkageController
from .RetargetingController import RetargetingController

import numpy as np

class EndpointRetargetingController(RetargetingController):
    
    def __init__(self, 
        src_model: OpenLinkage, 
        dest_model: OpenLinkage, 
        linkage_controller: LinkageController
    ):
        self.src_model = src_model
        self.dest_model = dest_model
        self.controller = linkage_controller

    def on_effectorpath_changed(self):
        # noop - kinematics are computed each frame.
        pass

    def on_trajectory_changed(self, trajectory):
        # noop - trajectory state isn't used; IK is computed each frame.
        pass

    def update(self, t: float, target_provider: SplineTargetProvider):
        if target_provider.is_valid():
            self.controller.update(self.src_model, target_provider.target)
            self.controller.update(self.dest_model, target_provider.dest_target(dest_index=0))
            
    
            
            
            
        
        