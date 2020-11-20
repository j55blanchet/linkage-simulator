
from typing import Tuple, List, Dict, Set

import numpy as np
from matplotlib.lines import Line2D
import matplotlib.collections

class LinkageNetwork:

    NodeIndex = int
    DistanceConstraint = Tuple[NodeIndex, NodeIndex, float]
    
    def __init__(self, nodes: List[np.array], distance_constraints: List[DistanceConstraint]):
        
        self.nodes = nodes
        self.distance_constraints = distance_constraints

        # Sanity Check
        for node in nodes:
            assert len(node) == 2
        for i, j, length in distance_constraints:
            assert 0 <= i < len(nodes)
            assert 0 <= j < len(nodes)
            assert i != j
            assert length > 0

    def draw(self, ax, prev: matplotlib.collections.LineCollection):
        
        segments = [
            (self.nodes[i], self.nodes[j]) 
            for i, j, _ in self.distance_constraints
        ]

        if prev:
            prev.set_segments(segments)
            return prev

        coll = matplotlib.collections.LineCollection(segments    )
        ax.add_collection(coll)
        return coll
        
        

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    # Defines a network that looks like:
    #
    #    x - x - x
    #    |   |   |
    #    x - x - x
    #
    network = LinkageNetwork(
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
        ]
    )

    fig, ax = plt.subplots()
    network.draw(ax, None)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 2)
    plt.show()