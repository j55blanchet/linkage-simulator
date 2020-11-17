
from matplotlib.lines import Line2D
import numpy as np
import math
import random
from typing import Tuple

from numpy.core.numeric import full
from numpy.lib.npyio import save

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

        buffer_percent = 0.02
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
    from .PathTargetProvider import PathTargetProvider
    from .ClickTargetProvider import ClickTargetProvider
    from .IKLinkageController import IKLinkageController
    from .DifferentialKinematicOpenLinkageController import DifferentialKinematicOpenLinkageController
    import random

    fps = 30
    full_circle_time = 4

    def testcase_2bar_ik():
        link = Linkage([1.3, 0.9], [0.1, 0.1])
        path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
        controller = IKLinkageController()
        driver = LinkageDriver(link, path_provider, controller)
        frames = np.linspace(0, 1, fps * full_circle_time)
        return driver, frames, True

    def testcase_2bar_diff():
        link = Linkage([1.3, 0.9], [0.1, 0.1])
        path_provider = PathTargetProvider([(1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)])
        controller = DifferentialKinematicOpenLinkageController()
        driver = LinkageDriver(link, path_provider, controller)
        frames = np.linspace(0, 1, fps * full_circle_time)
        return driver, frames, True
    
    def testcase_2bar_diff_click():
        link = Linkage([1.3, 0.9], [0.1, 0.1])
        path_provider = ClickTargetProvider(link.last_endpoint())
        controller = IKLinkageController()
        driver = LinkageDriver(link, path_provider, controller)
        frames = np.linspace(0, 1, fps * full_circle_time)
        return driver, frames, True
        
    def testcase_1():
        linkage = Linkage([3, 2, 1, 1.5, 2], [0.123, 0, math.radians(30), math.radians(-30), 0])
        path_provider = PathTargetProvider([linkage.last_endpoint(), (-4, 4), (-0.2, -2.3)])
        controller = DifferentialKinematicOpenLinkageController()

        driver = LinkageDriver(linkage, path_provider, controller)
        frames = np.linspace(0, 1, fps * full_circle_time)
        return driver, frames, True

    def testcase_2():
        bars = 8
        linkage = Linkage(
            link_sizes=[0.5 + 2 * random.random() for i in range(bars)], 
            link_angles=[-math.pi / 2 + math.pi * random.random() for i in range(bars)]
        )
        total_len = sum(linkage.links)
        safe_len = 0.9 * total_len / math.sqrt(2)
        
        path_provider = PathTargetProvider([(safe_len, safe_len), 
                                            (-safe_len, -safe_len),
                                            (-safe_len, 0.5 * safe_len), 
                                            (safe_len, -safe_len)])
        controller = DifferentialKinematicOpenLinkageController()

        driver = LinkageDriver(linkage, path_provider, controller)
        frames = np.linspace(0, 1, fps * full_circle_time * 2)
        return driver, frames, True

    def testcase_click(bars: int = 6):
        
        linkage = Linkage(
            link_sizes=[0.5 + 2 * random.random() for i in range(bars)], 
            link_angles=[-math.pi / 2 + math.pi * random.random() for i in range(bars)]
        )
        path_provider = ClickTargetProvider(linkage.last_endpoint())
        controller = DifferentialKinematicOpenLinkageController()

        driver = LinkageDriver(linkage, path_provider, controller)
        frames = None
        return driver, frames, False

    

    driver, frames, save_res = testcase_click()

    
    anim = PlotAnimator(driver, frames=frames)
    anim.run(fps=fps, save_res=save_res)
    


    