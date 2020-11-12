from .linkage_types import *
from matplotlib.lines import Line2D
from math import sqrt

class PathTargetProvider:
    def __init__(self, points: List[Point2d], loop: bool = True) -> None:
        
        if loop:
            points.append(points[0])
            
        self.points = points

        self.lengths = [
            sqrt(
                (points[i][0] - points[i+1][0])**2 + 
                (points[i][1] - points[i+1][1])**2
            )
            for i in range(len(points)-1)
        ]

        self.len_total = sum(self.lengths)

    def get_target(self, tt: float) -> Tuple[float, float]:
        t = tt % 1
        
        l = t * self.len_total
        

        l_sofar = 0
        for i, seg_length in enumerate(self.lengths):
            if l <= l_sofar + seg_length:
                dl = l - l_sofar
                seg_percent = dl / seg_length
                
                target = PathTargetProvider.interpolate(
                    self.points[i], 
                    self.points[i+1], 
                    seg_percent
                )
                print(f"{tt:.2f}: {t:.2f} ==> {target}")
                return target

            l_sofar += seg_length

        return self.points[-1]
        
    
    def draw(self, ax, target: Point2d, line: Line2D = None):
        x, y = target

        if line is None:
            return ax.plot([x], [y],  "ro", label="Target", marker='x')[0]
        
        line.set_data([x], [y])
        return line

    @staticmethod
    def interpolate(p1: Point2d, p2: Point2d, t: float) -> Point2d:
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = x2 - x1, y2 - y1
        return x1 + dx * t, y1 + dy * t
 