from math import sqrt

from .TargetProvider import *

class PathTargetProvider(TargetProvider):
    def __init__(self, points: List[np.array], loop: bool = True) -> None:
        
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
        self._target = points[0]

    def update_target(self, tt: float, dt: float):

        t = tt % 1
        l = t * self.len_total
        l_sofar = 0

        for i, seg_length in enumerate(self.lengths):
            if l <= l_sofar + seg_length:
                dl = l - l_sofar
                seg_percent = dl / seg_length
                
                self._target = TargetProvider.interpolate(
                    self.points[i], 
                    self.points[i+1], 
                    seg_percent
                )
                return

            l_sofar += seg_length

        self._target = self.points[-1]
        
    @property
    def target(self):
        return self._target
    
 