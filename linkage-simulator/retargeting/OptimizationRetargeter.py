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
import gurobipy
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
):
    state_count = len(src_trajectory.states)

    opt_model = gurobipy.Model('LinkageRetargeting')

    vars = []
    for t in range(state_count):
        time_t_vars = {}
        vars.append(time_t_vars)
        
        # WE DON"T NEED ALL THESE FOR THE SRC VARIABLES!!
        #   > THE TRAJECTORY IS GIVEN
        #     VEL & ACC ARE ONLY NEEDED FOR THE DESTINATION
        #     todo: refactor this out, update the problem statement. 
        #     goal: have a 2d retargeting demo working by 10am tomorrow.
        time_t_vars['ang'] = opt_model.addVars(
            [
                f'ang-{i}-{t}'
                for i in range(dest_model.link_count)
            ],
            vtype=gurobipy.GRB.CONTINUOUS,
            lb=dest_model.link_minangles,
            ub=dest_model.link_maxangles,
            obj=0,
            name=f"ang-{t}"
        )

        time_t_vars['angvel'] = opt_model.addVars(
            [
                f'angvel-{i}-{t}'
                for i in range(dest_model.link_count)
            ],
            vtype=gurobipy.GRB.CONTINUOUS,
            lb=-np.array(dest_model.link_maxspeeds),
            ub=dest_model.link_maxspeeds,
            obj=0,
            name=f"angvel-{t}"
        )

        # Variables for 
        time_t_vars['angacc'] = opt_model.addVars(
            [
                f'angacc-{i}-{t}'
                for i in range(dest_model.link_count)
            ],
            vtype=gurobipy.GRB.CONTINUOUS,
            lb=-np.array(dest_model.link_maxaccels),
            ub=dest_model.link_maxaccels,
            obj=0,
            name=f"angacc-{t}"
        )

        # Add constraint to link angular velocity and acceleration
        opt_model.addConstrs(
            (
                time_t_vars['angvel'][f'angvel-{i}-{t}'] - 
                (vars[t-1]['angvel'][f'angvel-{i}-{t - 1}'] if t > 0 else 0.)
                ==
                (vars[t-1]['angacc'][f'angacc-{i}-{t - 1}'] if t > 0 else 0.)
                for i in range(dest_model.link_count)
            ),
            name=f"angvel-angaccel-{t}"
        )

        # Add constraint to link rotation and angular velocity
        opt_model.addConstrs(
            (
                time_t_vars['ang'][f'ang-{i}-{t}'] - 
                (vars[t-1]['ang'][f'ang-{i}-{t - 1}'] if t > 0 else 0.)
                ==
                (vars[t-1]['angvel'][f'angvel-{i}-{t - 1}'] if t > 0 else 0.)
                for i in range(dest_model.link_count)
            ),
            name=f"ang-angvel-{t}"
        )

    opt_model.setObjective(
        sum([
            (   
                sum(src_trajectory.states[t][src_ii] for src_ii in range(src_i + 1)) -
                sum(vars[t]['ang'][f'ang-{dest_ii}-{t}'] for dest_ii in range(dest_i + 1))
            )**2
            for t in range(state_count)
            for src_i, dest_i in matched_links
        ]), 
        gurobipy.GRB.MINIMIZE
    )

    opt_model.optimize()

    if opt_model.status != gurobipy.GRB.OPTIMAL:
        raise Exception(f"Optimization failed with status {opt_model.status}")
    
    dest_trajectory = LinkageTrajectory()
    dest_trajectory.stateDuration = src_trajectory.stateDuration
    dest_trajectory.states = [
        [
            vars[t]['ang'][f'ang-{dest_i}-{t}'].x
            for dest_i in range(dest_model.link_count)
        ]
        for t in range(state_count)
    ]

    return dest_trajectory

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
        self.dest_trajectory = retarget_trajectory(
            self.src_model,
            trajectory,
            self.dest_model,
            self.matched_links,
            self.line_primitives,
        )
        print("Recalculated src trajectory")
        # Simply copy the src trajectory for now
        # self.dest_trajectory = trajectory
# 
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



if __name__ == "__main__":
    # TODO: write test case for optimizer.
    pass


    retargeted_trajectory = retarget_trajectory(
        src_model= OpenLinkage(
            link_sizes=[1.],
            link_angles=[0.],
            link_minangles=[-np.pi],
            link_maxangles=[np.pi],
            link_maxspeeds=[np.pi / 30.],
            link_maxaccels=[np.pi / 30. / 2.],
        ),
        src_trajectory= LinkageTrajectory(
            stateDuration=1./30.,
            states=[
                (0.,),
                (0.5,),
                (1.,),
            ]
        ),
        dest_model= OpenLinkage(
            link_sizes=[1.],
            link_angles=[0.],
            link_minangles=[-np.pi],
            link_maxangles=[np.pi],
            link_maxspeeds=[np.pi / 30.],
            link_maxaccels=[np.pi / 30. / 2.],
        ),
        matched_links=[
            (0, 0),
        ],
        line_primitives=[],
    )

    print(retargeted_trajectory)