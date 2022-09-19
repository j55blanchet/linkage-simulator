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
        src_trajectory: LinkageTrajectory,
        dest_model: OpenLinkage,
        matched_links: List[Tuple[int, int]],
        line_primitives: List[LinePrimitive],
    ):
        self.src_model = src_model
        self.src_trajectory = src_trajectory
        self.dest_model = dest_model
        self.matched_links = matched_links
        self.line_primitives = line_primitives
        self.dest_trajectory = None

    def on_trajectory_changed(self):
        self.dest_trajectory = retarget_trajectory(
            self.src_model,
            self.src_trajectory,
            self.dest_model,
            self.matched_links,
            self.line_primitives,
        )

    def update(self, frame: float):
        # TODO: set angles to the precalculated angle values
        pass