
from math import sqrt
from matplotlib.lines import Line2D
from .Linkage import Linkage
from typing import Tuple, List
import random
from .PlotAnimator import PlotAnimator
import numpy as np

Point2d = Tuple[float, float]

class LinkageDriver:
    def __init__(self, linkage: Linkage, target_provider) -> None:
        self.linkage = linkage
        self.ln_linkage = None
        self.ln_target = None
        self.target = (0, 0)
        self.target_provider = target_provider

    def get_plot_size(self) -> Tuple[float, float, float, float]:

        buffer_percent = 0.10
        link_maxlen = sum(self.linkage.links)

        size = (1 + buffer_percent) * link_maxlen
        return (-size, size, -size, size)


    def update(self, frame: float):
        spd = 0.01
        for i in range(len(self.linkage.angles)):
            self.linkage.angles[i] += spd * (-0.5 + random.random())

        self.target = self.target_provider.get_target(frame)
        

    def plot(self, ax) -> Tuple[Line2D]:
        self.ln_linkage = self.linkage.draw(ax, self.ln_linkage)
        self.ln_target = self.target_provider.draw(ax, self.target, self.ln_target)
        return self.ln_linkage, self.ln_target


class PathFollower:
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
                
                target = PathFollower.interpolate(
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
 


if __name__ == "__main__":
    linkage = Linkage([2, 1])
    path_provider = PathFollower([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
    driver = LinkageDriver(linkage, path_provider)
    anim = PlotAnimator(driver, frames=np.linspace(0, 4, 30*8))
    anim.run()


    