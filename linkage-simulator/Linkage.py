
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from typing import Generator, TypeVar, List, Iterable, Final
import math
import numpy as np

from .linkage_types import *


class Linkage:

    EQUALITY_THRESHOLD: float = 0.01
    EQUALITY_THRESHOLD_SQUARED: float = 0.01 * 0.01
    
    def __init__(self, link_sizes: Iterable[float], link_angles: Iterable[float]=None) -> None:

        self.links = tuple(link_sizes)

        if link_angles is None:
            self.angles = [0.0 for _ in self.links]
        else:
            self.angles = list(link_angles)
            assert len(link_angles) == len(self.links)

        assert len(self.links) > 0
    
    def is_closed(self) -> bool:
        x, y = Linkage.Helpers.get_last(self.endpoints())
        return x*x + y*y < Linkage.EQUALITY_THRESHOLD_SQUARED 

    def draw(self, ax, line: Line2D = None) -> List[Line2D]:
        # https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/
        x_cords, y_cords = tuple(zip(*self.endpoints()))
        if line is None:
            return ax.plot(x_cords, y_cords, linestyle='solid')[0]

        line.set_data(x_cords, y_cords)
        return line
        
    def links_sequence(self):
        return zip(self.links, self.angles)

    def set_angles(self, angles: Iterable[float]):
        self.angles = list(angles)
        assert len(angles) == len(self.links)

    def move_angles(self, angle_changes: Iterable[float]):
        assert len(angle_changes) == len(self.angles)
        for i in range(len(angle_changes)):
            self.angles[i] += angle_changes[i]

    def endpoints(self):
        x, y, ang = 0.0, 0.0, 0.0
        yield x, y
        for l, theta in self.links_sequence():
            ang += theta
            x += math.cos(ang) * l
            y += math.sin(ang) * l
            yield x, y

    def last_endpoint(self):
        return Linkage.Helpers.get_last(self.endpoints())

    def __str__(self) -> str:
        return f"Linkage: " + \
            ",".join((
                f"({l} @ {math.degrees(a)} deg)" 
                for (l, a) in self.links_sequence()
            ))

    class Helpers:

        T = TypeVar('T')
        @staticmethod
        def combined(*its: Iterable[T]) -> Iterable[T]:
            """Yields the values from each iterable in succession

            Args:
                *its (Iterable): First iterable to generate values from

            Yields:
                Generator[Any, None, None]: Generator with the values from all the iterables
            """
            for it in its:
                for i in it:
                    yield i
        
        @staticmethod
        def get_last(gen: Generator):
            last = None
            for val in gen:
                last = val
            return last

        @staticmethod
        def dist_squared(p1: Point2d, p2: Point2d):
            x1, y1 = p1
            x2, y2 = p2
            return (x2 - x1)**2 + (y2 - y1)**2

        @staticmethod
        def dist(p1: Point2d, p2: Point2d):
            return math.sqrt(Linkage.Helpers.dist_squared(p1, p2))

        @staticmethod
        def vector(fromP: Point2d, to: Point2d):
            x1, y1 = fromP
            x2, y2 = to
            return x2 - x1, y2 - y1

        @staticmethod
        def get_approach(fromP: Point2d, to: Point2d, max_d):
            if Linkage.Helpers.dist_squared(fromP, to) < max_d**2:
                return Linkage.Helpers.vector(fromP, to)
            
            dVector = Linkage.Helpers.vector(fromP, to)
            v = np.array(dVector)
            v = v / np.linalg.norm(v)
            v *= max_d
            return v[0], v[1]
            

    
if __name__ == "__main__":

    # Create equilateral triangle
    closed_linkage = Linkage([1, 1, 1], [0, math.pi * 2/3, math.pi * 2/3])
    assert closed_linkage.is_closed()

    open_linkage = Linkage([1, 1, 1], [0, math.pi / 2, -math.pi / 2])
    assert not open_linkage.is_closed()
    assert list(open_linkage.endpoints()) == [
        (0, 0),
        (1, 0),
        (1, 1),
        (2, 1)
    ]

    
    