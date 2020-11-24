
import scipy.linalg

from .LinkageController import *

class ConstraintController(LinkageController):
    def update(self, linkage: Linkage, target: np.array):
        assert isinstance(linkage, LinkageNetwork)
        
        linkage.rectify()

        # TODO: Don't find nullspace. Set equal to current distance
        #       error and set accordingly.
        #   see: https://mail.python.org/pipermail/scipy-user/2009-May/021308.html
        #  This could help us correct constraint errors while adjusting
        #  the linkage simultaneously.
        jacobian = linkage.constraint_jacobian()
        nullspace = scipy.linalg.null_space(jacobian)

        _, basis_vector_count = nullspace.shape

        # Subtract 0.5 to adjust the range of the coefficients to [-0.5, 0.5) rather than [0, 1)
        rand_coefficients = np.random.random_sample(basis_vector_count) - 0.5 
        action = np.matmul(nullspace, rand_coefficients)

        action /= np.linalg.norm(action)
        action *= 0.05
        
        assert len(action) == len(linkage.nodes) * 2
        for node_i in range(len(linkage.nodes)):
            dx = action[node_i * 2]
            dy = action[node_i * 2 + 1]
            linkage.nodes[node_i] += np.array((dx, dy))
            # print(f"Node {node_i: 2}: {dx:+.6}, {dy:+.6}")

        

    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        assert isinstance(linkage, LinkageNetwork)
        raise NotImplemented()

if __name__ == "__main__":
    test_network = LinkageNetwork(
        nodes = [
            (0, 0),
            (1, 0)
        ],
        distance_constraints = [
            (0, 1, 1)
        ],
        fixed_constraints=[
            (0, (0, 0))
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

        

    
        
        