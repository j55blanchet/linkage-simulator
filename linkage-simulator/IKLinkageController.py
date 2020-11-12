from math import cos, sqrt, atan2, acos, sin

from .LinkageController import *

def dist_squared(p1: Point2d, p2: Point2d):
    x1, y1 = p1
    x2, y2 = p2
    return (x2 - x1)**2 + (y2 - y1)**2

def dist(p1: Point2d, p2: Point2d):
    return sqrt(dist_squared(p1, p2))

class IKLinkageController(LinkageController):

    def __init__(self, tolerance: float = 1e-6) -> None:
        self.tolerance = tolerance

    def update(self, linkage: Linkage, target: Point2d):

        if len(linkage.links) > 2:
            raise NotImplemented("InverseKinematics contorller can only work with 1R or 2R linkages.")

        tx, ty = target

        if len(linkage.links) == 1:
            linkage.angles[0] = atan2(ty, tx)

        angs = self.inverse_kinematics(linkage, target)
        linkage.set_angles(angs)

    def meets_target(self, linkage: Linkage, target: Point2d) -> bool:
        if len(linkage.links) > 2:
            raise NotImplemented("InverseKinematics contorller can only work with 1R or 2R linkages.")

        tx, ty = target
        end_point = linkage.last_endpoint()

        return abs(dist_squared((0, 0), end_point)) < self.tolerance

    
    def inverse_kinematics(self, linkage: Linkage, target: Point2d) -> Tuple[float, float]:

        assert len(linkage.links) == 2

        x, y = target
        l1 = linkage.links[0]
        l2 = linkage.links[1]

        A_squared = dist_squared((0, 0), target)
        cos_ratio = (A_squared - l1**2 - l2**2) / (2 * l1 * l2)

        # This ratio will be > 1 when the target is beyond 
        # the reach of the arms. So we clamp it to fully extended
        cos_ratio = min(1, cos_ratio) 

        # This ration will be < -1 when the target is too close to 
        # the center. We clamp it to be fully inward.
        cos_ratio = max(-1, cos_ratio)

        # Note - flipping the sign of cos_ratio will give us 
        #        an alternate solution
        theta2 = acos(cos_ratio)

        B = atan2(l2 * sin(theta2), l1 + l2 * cos(theta2))
        C = atan2(y, x)

        theta1 = C - B
        return theta1, theta2
