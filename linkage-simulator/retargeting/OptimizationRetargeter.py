"""
    InterpretableOptimizationRetargeterV1.py

    First version of a retargeter for a toy problem involving two 2R arms with
    different lengths. Given a src armature & trajectory with pre-defined
    interpretability primitives, the goal is to calculate a target trajectory
    that is stylistically similar to the src trajectory but fitted to the target
    armature and emphasizing the interpretability primitives.

    Author: Julien Blanchet
"""
from dataclasses import dataclass
from typing import *
from ..model import OpenLinkage, LinkageTrajectory
from ..controller import LinkageController
from ..view import SplineTargetProvider
from .RetargetingController import RetargetingController
from gurobipy import Model, GRB
import numpy as np

@dataclass
class LinePrimitive:
    link_id: int
    start_time: float
    end_time: float
    strength: float

def retarget_trajectory(
    src_model: OpenLinkage,
    src_trajectory: LinkageTrajectory,
    dest_model: OpenLinkage,
    matched_links: List[Tuple[int, int]],
    line_primitives: List[LinePrimitive],
    
) -> LinkageTrajectory:




    pass


class OptimizationRetargetingController(RetargetingController):
    def __init__(
        self,
        src_model: OpenLinkage,
        src_controller: LinkageController,
        dest_model: OpenLinkage,
        matched_links: List[Tuple[int, int]],
        line_primitives: List[LinePrimitive],
    ):
        self.src_model = src_model
        self.src_controller = src_controller
        self.dest_model = dest_model
        self.matched_links = matched_links
        self.line_primitives = line_primitives
        self.dest_trajectory = None

    def on_effectorpath_changed(self):
        # Reset the trajectory - needs to be recalculated
        self.dest_trajectory = None
    
    def on_trajectory_changed(self, trajectory: LinkageTrajectory):
        # self.dest_trajectory = retarget_trajectory(
            # self.src_model,
            # self.src_trajectory,
            # self.dest_model,
            # self.matched_links,
            # self.line_primitives,
        # )
        # Simply copy the src trajectory for now
        self.dest_trajectory = trajectory

    def update(self, t: float, target_provider: SplineTargetProvider):

        # Update src
        self.src_controller.update(self.src_model, target_provider.target)

        if self.dest_trajectory is None:
            return
        
        dt = self.dest_trajectory.stateDuration
        i = int(t / dt)
        if i >= len(self.dest_trajectory.states):
            i = len(self.dest_trajectory.states) - 1
        if i < 0:
            i = 0
        
        state = self.dest_trajectory.states[i]

        # TODO: set angles to the precalculated angle values
        self.dest_model.set_angles(state)