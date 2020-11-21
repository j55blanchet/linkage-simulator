
import scipy.linalg

from .LinkageController import *

class ConstraintController(LinkageController):
    def update(self, linkage: Linkage, target: np.array):
        assert isinstance(linkage, LinkageNetwork)
        

        # TODO: Don't find nullspace. Set equal to current distance
        #       error and set accordingly.
        #   see: https://mail.python.org/pipermail/scipy-user/2009-May/021308.html
        #  This could help us correct constraint errors while adjusting
        #  the linkage simultaneously.
        jacobian = self._constraint_jacobian(linkage)
        nullspace = scipy.linalg.null_space(jacobian)

        _, basis_vector_count = nullspace.shape
        rand_coefficients = np.random.rand(basis_vector_count)
        action = np.matmul(nullspace, rand_coefficients)
        
        assert len(action) == len(linkage.nodes) * 2
        for node_i in range(len(linkage.nodes)):
            dx = action[node_i * 2]
            dy = action[node_i * 2 + 1]
            linkage.nodes[node_i] += np.array((dx, dy))
            print(f"Node {node_i: 2}: {dx:+.6}, {dy:+.6}")

    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        assert isinstance(linkage, LinkageNetwork)
        raise NotImplemented()

    def _constraint_jacobian(self, linkage: LinkageNetwork):
        
        return np.array([
            self._distance_constraint_partials(linkage, i)
            for i in range(len(linkage.distance_constraints))
        ])

    def _distance_constraint_partials(self, 
            linkage: LinkageNetwork, 
            constraint_index: int) -> np.array:

        variable_count = len(linkage.nodes) * 2
        
        # Distance constraint is in the form of:
        # g(i, j) = (xj - xi)^2 + (yj - yi)^2 = distance
        # in the general form, we have:
        #   1. d/da of (a-b)^2 = 2(a-b)
        #   2. d/db of (a-b)^2 = 2(b-a)
        #
        # Therefore:
        #    dg/dxj = 2(xj - xi)
        #    dg/dxi = 2(xi - xj)
        #    dg/dyj = 2(yj - yi)
        #    dg/dyi = 2(yi - yj)
        i, j, distance = linkage.distance_constraints[constraint_index]
        xi, yi = linkage.nodes[i]
        xj, yj = linkage.nodes[j]
        
        partials = np.zeros(variable_count)
        partials[i*2] = 2 * (xi - xj)     # dg/dxi
        partials[j*2] = 2 * (xj - xi)     # dg/dxj
        partials[i*2 + 1] = 2 * (yi - yj) # dg/dyi
        partials[j*2 + 1] = 2 * (yj - yi) # dg/dyj

        return partials



if __name__ == "__main__":
    test_network = LinkageNetwork(
        nodes = [
            (0, 0),
            (1, 0)
        ],
        distance_constraints = [
            (0, 1, 1)
        ],
        bounds=(-1, 2, -1, 2)
    )
    # test_network = LinkageNetwork(
    #     nodes=[
    #         (-1, -1),
    #         (-1, 1),
    #         (1, 1),
    #         (1, -1)
    #     ],
    #     distance_constraints=[
    #         (0, 1, 2), (1, 2, 2), (2, 3, 2), (3, 0, 2)
    #     ],
    #     bounds=(-2, 2, -2, 2)
    # )
    controller = ConstraintController()
    controller.update(test_network, np.array([1.01, 0]))
    print(test_network)
    # controller.

        

    
        
        