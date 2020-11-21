
import random
import math

import numpy as np

from .LinkageDriver import *

fps = 30
full_circle_time = 4

def testcase_2bar_ik():
    link = OpenLinkage([1.3, 0.9], [0.1, 0.1])
    path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
    controller = IKLinkageController()
    driver = LinkageDriver(link, path_provider, controller)
    frames = np.linspace(0, 1, fps * full_circle_time)
    return driver, frames, True

def testcase_2bar_diff():
    link = OpenLinkage([1.3, 0.9], [0.1, 0.1])
    path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
    controller = DifferentialKinematicOpenLinkageController()
    driver = LinkageDriver(link, path_provider, controller)
    frames = np.linspace(0, 1, fps * full_circle_time)
    return driver, frames, True

def testcase_2bar_diff_click():
    link = OpenLinkage([1.3, 0.9], [0.1, 0.1])
    path_provider = ClickTargetProvider(link.last_endpoint())
    controller = IKLinkageController()
    driver = LinkageDriver(link, path_provider, controller)
    frames = np.linspace(0, 1, fps * full_circle_time)
    return driver, frames, True
    
def testcase_1():
    linkage = OpenLinkage([3, 2, 1, 1.5, 2], [0.123, 0, math.radians(30), math.radians(-30), 0])
    path_provider = PathTargetProvider([linkage.last_endpoint(), (-4, 4), (-0.2, -2.3)])
    controller = DifferentialKinematicOpenLinkageController()

    driver = LinkageDriver(linkage, path_provider, controller)
    frames = np.linspace(0, 1, fps * full_circle_time)
    return driver, frames, True

def testcase_2():
    bars = 8
    linkage = OpenLinkage(
        link_sizes=[0.5 + 2 * random.random() for i in range(bars)], 
        link_angles=[-math.pi / 2 + math.pi * random.random() for i in range(bars)]
    )
    total_len = sum(linkage.links)
    safe_len = 0.9 * total_len / math.sqrt(2)
    
    path_provider = PathTargetProvider([(safe_len, safe_len), 
                                        (-safe_len, -safe_len),
                                        (-safe_len, 0.5 * safe_len), 
                                        (safe_len, -safe_len)])
    controller = DifferentialKinematicOpenLinkageController()

    driver = LinkageDriver(linkage, path_provider, controller)
    frames = np.linspace(0, 1, fps * full_circle_time * 2)
    return driver, frames, True

def testcase_click(bars: int = 6):
    
    linkage = OpenLinkage(
        link_sizes=[0.5 + 2 * random.random() for i in range(bars)], 
        link_angles=[-math.pi / 2 + math.pi * random.random() for i in range(bars)]
    )
    path_provider = ClickTargetProvider(linkage.last_endpoint())
    controller = DifferentialKinematicOpenLinkageController()

    driver = LinkageDriver(linkage, path_provider, controller)
    frames = None
    return driver, frames, False

def testcase_constraint():
    # A "box" linkage
    linkage = LinkageNetwork(
        nodes=[(0, 0), (1, 0), (1, 1), (0, 1)],
        distance_constraints=[
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (3, 0, 1)
        ],
        bounds=(-5, 6, -5, 6)
    )

    path_provider = ClickTargetProvider((1, 1))
    controller = ConstraintController()
    driver = LinkageDriver(linkage, path_provider, controller)
    return driver, None, False

driver, frames, save_res = testcase_constraint()
anim = PlotAnimator(driver, frames=frames)
anim.run(fps=fps, save_res=False)