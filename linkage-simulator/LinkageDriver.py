
from matplotlib.lines import Line2D
import numpy as np
import math
import random
from typing import Tuple

from .Linkage import Linkage
from .LinkageController import LinkageController

from .TargetProvider import TargetProvider

class LinkageDriver:
    def __init__(self, linkage: Linkage, target_provider: TargetProvider, controller: LinkageController) -> None:
        self.linkage = linkage
        self.controller = controller
        self.ln_linkage = None
        self.ln_target = None
        self.target_provider = target_provider
        self.pframe = 0

    def get_plot_size(self) -> Tuple[float, float, float, float]:

        buffer_percent = 0.10
        link_maxlen = sum(self.linkage.links)

        size = (1 + buffer_percent) * link_maxlen
        return (-size, size, -size, size)


    def update(self, frame: float):
        dframe = frame - self.pframe
        self.target_provider.update_target(frame, dframe)
        self.controller.update(self.linkage, self.target_provider.target)
        self.pframe = frame
        

    def plot(self, ax) -> Tuple[Line2D]:
        self.ln_linkage = self.linkage.draw(ax, self.ln_linkage)
        self.ln_target = self.target_provider.draw(ax, self.ln_target)
        return self.ln_linkage, self.ln_target

    def button_clicked(self, x, y):
        self.target_provider.button_clicked(x, y)

if __name__ == "__main__":
    from .PlotAnimator import PlotAnimator
    # from .PathTargetProvider import PathTargetProvider
    from .ClickTargetProvider import ClickTargetProvider
    # from .IKLinkageController import IKLinkageController
    from .DifferentialKinematicOpenLinkageController import DifferentialKinematicOpenLinkageController

    linkage = Linkage([3, 2, 1, 1.5, 2], [0.123, 0, math.radians(30), math.radians(-30), 0])
    # path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
    path_provider = ClickTargetProvider(linkage.last_endpoint())
    ik_controller = DifferentialKinematicOpenLinkageController()

    driver = LinkageDriver(linkage, path_provider, ik_controller)

    fps = 60
    full_circle_time = 8
    anim = PlotAnimator(driver, frames=np.linspace(0, 1, fps*full_circle_time))
    anim.run(fps=fps)


    