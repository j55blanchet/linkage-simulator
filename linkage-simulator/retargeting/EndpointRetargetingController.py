from ..model import OpenLinkage
from ..view import SplineTargetProvider
from ..controller import LinkageController
from .RetargetingController import RetargetingController

import numpy as np

class EndpointRetargetingController(RetargetingController):
    
    def __init__(self, 
        src_model: OpenLinkage, 
        dest_model: OpenLinkage, 
        target_provider: SplineTargetProvider,
        linkage_controller: LinkageController
    ):
        self.src_model = src_model
        self.dest_model = dest_model
        self.target_provider = target_provider
        self.controller = linkage_controller

    def on_trajectory_changed(self):
        # noop - kinematics are computed each frame.
        pass

    def update(self, frame: float):
        if self.target_provider.is_valid():
            self.controller.update(self.src_model, self.target_provider.target)
            self.controller.update(self.dest_model, self.target_provider.dest_target(dest_index=0))
            
    
            
            
            
        
        