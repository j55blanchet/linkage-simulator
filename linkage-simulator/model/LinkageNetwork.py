
from typing import Tuple, List, Union, Sequence

import numpy as np
import matplotlib.collections
from matplotlib.artist import Artist
from matplotlib.axes import Axes

from .Linkage import Linkage

class LinkageNetwork(Linkage):

    Point = Union[Tuple[float, float], np.array]
    NodeIndex = int
    DistanceConstraint = Tuple[NodeIndex, NodeIndex, float]
    FixedConstraint = Tuple[NodeIndex, Point]
    
    def __init__(self, nodes: List[Point], 
        distance_constraints: List[DistanceConstraint], 
        bounds: Linkage.Bounds,
        fixed_constraints: List[FixedConstraint]):
        
        self.nodes = [np.array(node, float) for node in nodes] # ensure all nodes are numpy arrays
        self.distance_constraints = distance_constraints
        self.fixed_constraints = fixed_constraints
        self.bounds = bounds

        fixed_nodes = (i for i, _ in fixed_constraints)
        self.fixed_nodes = set(fixed_nodes)

        # Sanity Check
        for node in nodes:
            assert len(node) == 2
        for i, j, length in distance_constraints:
            assert 0 <= i < len(nodes)
            assert 0 <= j < len(nodes)
            assert i != j
            assert length > 0

    def draw(self, ax: Axes, prev: Sequence[Artist]) -> Sequence[Artist]:
        
        segments = [
            (self.nodes[i], self.nodes[j]) 
            for i, j, _ in self.distance_constraints
        ]

        fixed = [loc for _, loc in self.fixed_constraints]

        if prev:
            prev[0].set_segments(segments)
            prev[1].set_offsets(self.nodes)
            prev[2].set_offsets(fixed)
            return prev

        lines_coll = matplotlib.collections.LineCollection(segments)
        ax.add_collection(lines_coll)

        x, y = zip(*self.nodes)
        nodes_plt = ax.scatter(x, y)

        fixed_x, fixed_y = zip(*fixed)
        fixed_plt = ax.scatter(fixed_x, fixed_y)
        return lines_coll, nodes_plt, fixed_plt

    def get_plot_bounds(self) -> Tuple[float, float, float, float]:
        return self.bounds

    def satisfies_distance_constraint(self, constraint_index: int) -> bool:
        raise NotImplemented()

    def satisfies_fixed_constraint(self, constraint_index: int) -> bool:
        raise NotImplemented()

    def satisfies_all_constraints(self) -> bool:
        
        for i in range(len(self.distance_constraints)):
            if not self.satisfies_distance_constraint(i):
                return False

        for i in range(len(self.fixed_constraints)):
            if not self.satisfies_fixed_constraint(i):
                return False

        return True

    def is_fixed_node(self, node_index: int) -> bool:
        return node_index in self.fixed_nodes
    
    @property
    def node_count(self) -> int:
        return len(self.nodes)
    
    @property
    def variable_count(self) -> int:
        return self.node_count * 2

    def rectify(self):
        jacobian = self.constraint_jacobian()
        
        errors = [
            self.distance_constraint_error(i)
            for i in range(len(self.distance_constraints))
        ]

        for i in range(len(self.fixed_constraints)):
            errors.extend(self.fixed_consraint_error(i))

        errors = np.array([errors]).T
        dx = -errors
        changes, residuals, rank, singulars = np.linalg.lstsq(jacobian, dx, rcond=None) 

        for i in range(self.node_count):
            dx = changes[i*2][0]
            dy = changes[i*2 + 1][0]
            self.nodes[i] = self.nodes[i] + np.array((dx, dy), float)
        
        return changes

    def constraint_jacobian(self):
        
        jacobian_distance = [
            self.distance_constraint_partial_derivs(i)
            for i in range(len(self.distance_constraints))
        ]

        jacobian_fixed = []
        for i in range(len(self.fixed_constraints)):
            jacobian_fixed.extend(
                self.fixed_constraint_partial_derivs(i)
            )    
        
        jacobian = jacobian_distance
        jacobian.extend(jacobian_fixed)
        return np.array(jacobian)
    
    def fixed_constraint_partial_derivs(self, constraint_index: int) -> np.array:

        # Fixed constraint can be expressed as:
        # g_x(i) = xi = 0
        # g_y(i) = yi = 0
        # 
        # Therefore:
        #   dg_x/di = 1
        #   dg_y/di = 1
        # 
        # Another way to put this: we include row in the jacobian 
        # that forces the x and y variables for this node not to change 
        node_i, _ = self.fixed_constraints[constraint_index]

        partials_x = np.zeros(self.variable_count)
        partials_x[node_i*2] = 1

        partials_y = np.zeros(self.variable_count)
        partials_y[node_i*2 + 1] = 1

        return partials_x, partials_y

    def distance_constraint_partial_derivs(self, constraint_index: int) -> np.array:
        
        # Distance constraint is in the form of:
        # g(i, j) = (xj - xi)^2 + (yj - yi)^2 = distance^2
        # in the general form, we have:
        #   1. d/da of (a-b)^2 = 2(a-b)
        #   2. d/db of (a-b)^2 = 2(b-a)
        #
        # Therefore:
        #    dg/dxj = 2(xj - xi)
        #    dg/dxi = 2(xi - xj)
        #    dg/dyj = 2(yj - yi)
        #    dg/dyi = 2(yi - yj)
        i, j, _ = self.distance_constraints[constraint_index]
        xi, yi = self.nodes[i]
        xj, yj = self.nodes[j]
        
        partials = np.zeros(self.variable_count)
        partials[i*2] = (xi - xj)     # dg/dxi
        partials[j*2] = (xj - xi)     # dg/dxj
        partials[i*2 + 1] = (yi - yj) # dg/dyi
        partials[j*2 + 1] = (yj - yi) # dg/dyj

        return partials
        
    def distance_constraint_error(self, constraint_index: int) -> float:
        i, j, constraint_distance = self.distance_constraints[constraint_index]
        node_i = self.nodes[i]
        node_j = self.nodes[j]
        return np.linalg.norm(node_j - node_i) - constraint_distance

    def fixed_consraint_error(self, constraint_index: int) -> Tuple[float, float]:
        i, fixed_loc = self.fixed_constraints[constraint_index]
        nodex, nodey = self.nodes[i]
        fixedx, fixedy = np.array(fixed_loc)
        return nodex - fixedx, nodey - fixedy

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
        ],
        fixed_constraints=[],
        bounds=(-1.1, 3.1, -1.1, 2.1)
    )

    fig, ax = plt.subplots()
    network.draw(ax, None)
    ax.set_xlim(-1, 3)
    ax.set_ylim(-1, 2)
    plt.show()


