
from matplotlib.lines import Line2D
import numpy as np
import random
from typing import Tuple

from .Linkage import Linkage
from .LinkageController import LinkageController
from .IKLinkageController import IKLinkageController
from .PlotAnimator import PlotAnimator
from .PathTargetProvider import PathTargetProvider

class LinkageDriver:
    def __init__(self, linkage: Linkage, target_provider, controller: LinkageController) -> None:
        self.linkage = linkage
        self.controller = controller
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
        self.controller.update(self.linkage, self.target)
        

    def plot(self, ax) -> Tuple[Line2D]:
        self.ln_linkage = self.linkage.draw(ax, self.ln_linkage)
        self.ln_target = self.target_provider.draw(ax, self.target, self.ln_target)
        return self.ln_linkage, self.ln_target

if __name__ == "__main__":
    linkage = Linkage([2, 1])
    path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
    ik_controller = IKLinkageController()

    driver = LinkageDriver(linkage, path_provider, ik_controller)
    
    anim = PlotAnimator(driver, frames=np.linspace(0, 4, 30*8))
    anim.run()


    