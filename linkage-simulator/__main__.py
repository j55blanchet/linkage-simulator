
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
        fixed_constraints=[
            (0, (0, 0))
        ],
        bounds=(-5, 6, -5, 6)
    )

    path_provider = ClickTargetProvider((0, 0))
    controller = ConstraintController()
    driver = LinkageDriver(linkage, path_provider, controller)
    return driver, None, False

def testcase_constraint_8linkage():
    # A "8" linkage
    linkage = LinkageNetwork(
        nodes= [
            np.array([0, 0]),
            np.array([1, 0]),
            np.array([2, 0]),
            np.array([2, 1]),
            np.array([1, 1]),
            np.array([0, 1])
        ],
        distance_constraints=[
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (3, 4, 1),
            (4, 5, 1),
            (5, 0, 1),
            (1, 4, 1)
        ],
        fixed_constraints=[
            (2, (2, 0))
        ],
        bounds=(-2, 4, -2, 3)
    )

    path_provider = ClickTargetProvider((2, 0))
    controller = ConstraintController()
    driver = LinkageDriver(linkage, path_provider, controller)
    return driver, 180, True

def testcase_constraint_dynamicnetwork():
        # A "8" linkage
    linkage = LinkageNetwork(
        nodes= [
            np.array([0, 0]),   # 0
            np.array([1, 0]),   # 1
            np.array([4.5, 0]), # 2
            np.array([2.5, 1]), # 3
            np.array([3.5, 2]), # 4
            np.array([1.1, 2]), # 5
            np.array([0, 1.9]), # 6
            np.array([0.8, 1.3])# 7
        ],
        distance_constraints=[
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (3, 4, 1),
            (4, 5, 1),
            (5, 6, 1),
            (6, 0, 1),
            (0, 7, 1),
            (4, 7, 1)
        ],
        fixed_constraints=[
            (1, (1, 0))
        ],
        bounds=(-2, 7, -2, 4)
    )

    path_provider = ClickTargetProvider((1, 0))
    controller = ConstraintController()
    driver = LinkageDriver(linkage, path_provider, controller)
    return driver, 180, True


def test_rectification():
    # Test rectification
    network2 = LinkageNetwork(
        nodes = [
            np.array([0, 0]),
            np.array([1, 0]),
        ],
        distance_constraints=[
            (0, 1, 1)
        ],
        fixed_constraints=[
            (0, (0, 0))
        ],
        bounds=(-4, 4, -4, 4)
    )

    # print("Before rectification:", network2.nodes)
    # changes = network2.rectify()
    # assert np.allclose(changes, [0, 0, 0, 0])

    network2.distance_constraints[0] = (0, 1, 1.05)
    changes = network2.rectify()
    assert np.allclose(changes, np.array([[0], [0], [0.05], [0]]))
    print("After rectification", network2.nodes)

test = testcase_constraint_8linkage
driver, frames, save_res = test()
anim = PlotAnimator(driver, frames=frames)
anim.run(fps=fps, show=True, save=False, filename=test.__name__, repeat=False)