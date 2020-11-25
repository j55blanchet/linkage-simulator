
import scipy.linalg
import matplotlib.artist

from .LinkageController import *

class ConstraintController(LinkageController):

    def update(self, linkage: Linkage, target: np.array):
        assert isinstance(linkage, LinkageNetwork)
        
        action = self.get_action(linkage, target)
        self.perform_action(linkage, action)

        for i in range(4):
            linkage.rectify()
        # self.move_randomly(linkage)
        # self.project_onto_nullspace()

    def get_action(self, linkage: LinkageNetwork, target: np.array):

        # Find closest node to target
        inode = min(range(linkage.node_count), key=lambda i: np.linalg.norm(linkage.nodes[i] - target))

        # Move that node to the target
        dx, dy = target - linkage.nodes[inode]
        action = np.zeros(linkage.variable_count)
        action[inode * 2] = dx
        action[inode * 2 + 1] = dy
        
        return action

    def move_randomly(self, linkage: LinkageNetwork):
        jacobian = linkage.constraint_jacobian()
        nullspace = scipy.linalg.null_space(jacobian)

        _, basis_vector_count = nullspace.shape

        # Subtract 0.5 to adjust the range of the coefficients to [-0.5, 0.5) rather than [0, 1)
        rand_coefficients = np.random.random_sample(basis_vector_count) - 0.5 
        action = np.matmul(nullspace, rand_coefficients)

        action /= np.linalg.norm(action)
        action *= 0.05
        self.perform_action(linkage, action)

    def perform_action(self, linkage: LinkageNetwork, action: np.array):
        assert len(action) == len(linkage.nodes) * 2
        for node_i in range(len(linkage.nodes)):
            dx = action[node_i * 2]
            dy = action[node_i * 2 + 1]
            linkage.nodes[node_i] += np.array((dx, dy))
    
    def project_onto_nullspace(self, linkage: LinkageNetwork, action: np.array):
        # See: https://mail.python.org/pipermail/scipy-user/2009-May/021308.html
        jacobian = linkage.constraint_jacobian()
        nullspace = scipy.linalg.null_space(jacobian)
        projected_action = nullspace * np.dot(nullspace, action[:,np.newaxis]).sum(axis=0)
        return projected_action

    def meets_target(self, linkage: Linkage, target: np.array) -> bool:
        assert isinstance(linkage, LinkageNetwork)
        raise NotImplemented()

    def draw(self, ax, cached) -> List[matplotlib.artist.Artist]:
        return []

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

        

    
        
        