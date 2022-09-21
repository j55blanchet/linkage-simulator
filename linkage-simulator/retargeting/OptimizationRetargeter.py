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

    vars = {}

    for name, model, trajectory in [('src', src_model, src_trajectory), ('dest', dest_model, None)]:
        vars[name] = []
        for t in range(state_count):
            time_t_vars = {}
            vars[name].append(time_t_vars)
            
            # WE DON"T NEED ALL THESE FOR THE SRC VARIABLES!!
            #   > THE TRAJECTORY IS GIVEN
            #     VEL & ACC ARE ONLY NEEDED FOR THE DESTINATION
            #     todo: refactor this out, update the problem statement. 
            #     goal: have a 2d retargeting demo working by 10am tomorrow.
            time_t_vars['ang'] = opt_model.addVars(
                [
                    f'{name}-ang-{i}-{t}'
                    for i in range(model.link_count)
                ],
                vtype=gurobipy.GRB.CONTINUOUS,
                lb=trajectory.states[t] if trajectory is not None else model.link_minangles,
                ub=trajectory.states[t] if trajectory is not None else model.link_maxangles,
                obj=0,
                name=f"{name}-ang-{t}"
            )

            time_t_vars['angvel'] = opt_model.addVars(
                [
                    f'{name}-angvel-{i}-{t}'
                    for i in range(model.link_count)
                ],
                vtype=gurobipy.GRB.CONTINUOUS,
                lb=-np.array(model.link_maxspeeds),
                ub=model.link_maxspeeds,
                obj=0,
                name=f"{name}-angvel-{t}"
            )

            # Variables for 
            time_t_vars['angacc'] = opt_model.addVars(
                [
                    f'{name}-angacc-{i}-{t}'
                    for i in range(model.link_count)
                ],
                vtype=gurobipy.GRB.CONTINUOUS,
                lb=-np.array(model.link_maxaccels),
                ub=model.link_maxaccels,
                obj=0,
                name=f"{name}-angacc-{t}"
            )

            # Add constraint to link angular velocity and acceleration
            opt_model.addConstrs(
                (
                    time_t_vars['angvel'][f'{name}-angvel-{i}-{t}'] - 
                    (vars[name][t-1]['angvel'][f'{name}-angvel-{i}-{t - 1}'] if t > 0 else 0.)
                    ==
                    (vars[name][t-1]['angacc'][f'{name}-angacc-{i}-{t - 1}'] if t > 0 else 0.)
                    for i in range(model.link_count)
                ),
                name=f"{name}-angvel-angaccel-{t}"
            )

            # Add constraint to link rotation and angular velocity
            opt_model.addConstrs(
                (
                    time_t_vars['ang'][f'{name}-ang-{i}-{t}'] - 
                    (vars[name][t-1]['ang'][f'{name}-ang-{i}-{t - 1}'] if t > 0 else 0.)
                    ==
                    (vars[name][t-1]['angvel'][f'{name}-angvel-{i}-{t - 1}'] if t > 0 else 0.)
                    for i in range(model.link_count)
                ),
                name=f"{name}-ang-angvel-{t}"
            )

    opt_model.setObjective(
        sum([
            (   vars['src'][t]['ang'][f'src-ang-{src_i}-{t}'] - 
                vars['dest'][t]['ang'][f'dest-ang-{dest_i}-{t}']
            )**2
            for t in range(state_count)
            for src_i, dest_i in matched_links
        ]), 
        gurobipy.GRB.MINIMIZE
    )

    opt_model.optimize()
    return opt_model

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