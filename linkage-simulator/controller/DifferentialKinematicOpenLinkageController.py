
import math
from typing import Literal, Union
import numpy as np
from math import pi, sin, cos

from .LinkageController import OpenLinkage, LinkageController

class DifferentialKinematicOpenLinkageController(LinkageController):
    MAX_MOVEMENT = 1e9

    def __init__(self) -> None:
        pass

    def update(self, linkage: OpenLinkage, target: np.array):

        dx, dy = target - linkage.last_endpoint()
        
        solution, residuals, rank, s = self.get_solution(linkage, dx, dy)
        
        if rank < 2:
            print("ALERT! Singular config")

        solution_norm = np.linalg.norm(solution)

        if solution_norm > DifferentialKinematicOpenLinkageController.MAX_MOVEMENT:
            solution = solution / solution_norm * DifferentialKinematicOpenLinkageController.MAX_MOVEMENT
        
        linkage.move_angles(solution)

    def get_solution(self, linkage: OpenLinkage, dx: float, dy: float):
        jacobian = self.compute_jacobian(linkage)
        dX = np.array((dx, dy))
        return np.linalg.lstsq(jacobian, dX, rcond=None) 

    def meets_target(self, linkage: OpenLinkage, target: np.array) -> bool:
        return OpenLinkage.Helpers.dist(linkage.last_endpoint(), target) < 1e-4

    def compute_jacobian(self, linkage: OpenLinkage):

        clinks = len(linkage.angles)

        x_factors = [
            -linkage.links[i] * sin(sum(linkage.angles[0:i+1]))
            for i in range(clinks)
        ]
        y_factors = [
            linkage.links[i] * cos(sum(linkage.angles[0:i+1]))
            for i in range(clinks)
        ]

        return np.array([
            [sum(x_factors[-clinks + i:]) for i in range(0, clinks)],
            [sum(y_factors[-clinks + i:]) for i in range(0, clinks)]
        ])

if __name__ == "__main__":

    print("DifferentialKinematicOpenLinkageController tests")
    print()
    controller = DifferentialKinematicOpenLinkageController()

    print("== Validating Jacobian ==")
    link = OpenLinkage(
        link_sizes=[2,1],
        link_angles=[0, math.radians(90)]
    )
    print(link)
    jacob = controller.compute_jacobian(link)
    expected = np.array([
        [-1, -1],
        [2,   0]
    ])
    print(f"Expected:\n{expected}")
    print(f"Got:\n{jacob}")
    matched_expected = np.allclose(jacob, expected)
    print(f"Test {'Succeeded' if matched_expected else 'Failed'}")
    assert matched_expected
    print()

    print("== Validating Solution (leftwards) == ")
    sol, _, _, _ = controller.get_solution(link, -1, 0)
    got = sol
    expected = np.array([0, 1])
    matched_expected = np.allclose(got, expected)
    print(f"Expected:\n{expected}")
    print(f"Got:\n{got}")
    print(f"Test {'Succeeded' if matched_expected else 'Failed'}")
    assert matched_expected
    
    print()

    test_linkages = [
        ("Twobar Right Angle", OpenLinkage(
            link_sizes=[1,1], 
            link_angles=[0, pi / 2]
        )),
        ("Twobar Straight Singular", OpenLinkage(
            link_sizes=[1,1],
            link_angles=[0, 0]
        )),
        ("Three Bar Straight Singular", OpenLinkage(
            link_sizes=[1,1,1],
            link_angles=[0,0,0]
        )),
        ("Three Bar Semi Singular", OpenLinkage(
            link_sizes=[1,1,1],
            link_angles=[0, pi, 90]
        )),
        ("Three Bar Non-Singular", OpenLinkage(
            link_sizes=[1,1,1],
            link_angles=[20, 20, 20]
        ))
    ]

    for name, linkage in test_linkages:
        print(name)
        jacobian = controller.compute_jacobian(linkage)
        print("Linkage: ", linkage)
        rank = np.linalg.matrix_rank(jacobian)
        print(jacobian)
        print("Rank", rank)
        print()
    

    print()
    print("Twobar Right Angle - solving")
    link = OpenLinkage(
        link_sizes=[1,1], 
        link_angles=[0, pi / 2]
    )

    for dx, dy in [(0, 0.01), (0.01, 0), (-0.01, 0), (0, -0.01)]:
        res, residuals, rank, s = controller.get_solution(link, dx, dy)
        dx, dy = res
        print(f"{dx}, {dy}: solution", res)
        print(f"==> dt1, dt2 == {dx},{dy}")

    print("\n")
    print("1 bar linkage-solving (straight up)")
    link = OpenLinkage(
        link_sizes=[1],
        link_angles=[0]
    )
    solution, residuals, rank, s = controller.get_solution(link, dx=0, dy=0)
    print(f"solution", solution)