from typing import *
import random
import math
import numpy as np
from matplotlib.lines import Line2D

from ..model.OpenLinkage import OpenLinkage
from ..drivers.DriverBase import DriverBase
from ..view.SplineTargetProvider import SplineTargetProvider

from .RetargetingController import RetargetingController

class RetargetingDriver(DriverBase):

    def __init__(self, 
        linkage_src: OpenLinkage, 
        linkage_dest: OpenLinkage,
        target_provider:  SplineTargetProvider,
        retargeting_controller: RetargetingController,
    ) -> None:
        self.linkage_src = linkage_src
        self.linkage_dest = linkage_dest
        self.target_provider = target_provider
        self.retargeting_controller = retargeting_controller

        self.plot_size = self.calculate_plot_size()
        self.origin_src = self.plot_size[0] / 2, 0.0 # 25% x, center y
        self.origin_dest = self.plot_size[1] / 2, 0.0 # 75% x, center y
        self.target_provider.src_origin = self.origin_src
        self.target_provider.add_retargeting(
            origin=self.origin_dest,
            scale=self.linkage_dest.length / self.linkage_src.length
        )

        self.ln_linkage_src = None
        self.ln_linkage_dest = None
        self.ln_target_prov = None
        self.pframe = 0.0

    def calculate_plot_size(self) -> Tuple[float, float, float, float]:
        sx_min, sx_max, sy_min, sy_max = self.linkage_src.get_plot_bounds()
        dx_min, dx_max, dy_min, dy_max = self.linkage_dest.get_plot_bounds()

        # plot the two charts side by side
        half_width = max(sx_max, dx_max) - min(sx_min, dx_min)
        height = max(sy_max, dy_max) - min(sy_min, dy_min)
        return -half_width, half_width, -height/2, height/2

    def get_plot_size(self) -> Tuple[float, float, float, float]:
        return self.plot_size

    def update(self, frame: float):
        dt = frame - self.pframe
        self.target_provider.update_target(frame, dt)
        self.retargeting_controller.update(frame)
        self.pframe = frame
    
    def plot(self, ax) -> Tuple[Line2D]:
        self.ln_linkage_src = self.linkage_src.draw(ax, self.ln_linkage_src, offset=self.origin_src)
        self.ln_linkage_dest = self.linkage_dest.draw(ax, self.ln_linkage_dest, offset=self.origin_dest)
        self.ln_target_prov = self.target_provider.draw(ax, self.ln_target_prov, offset=(0.0, 0.0))
        return (*self.ln_linkage_src, *self.ln_linkage_dest, *self.ln_target_prov)
    
    def mouse_pressed(self, x, y, e):
        print(f"Button Click: {x}, {y}")
        self.target_provider.button_clicked(x, y)
        self.retargeting_controller.on_trajectory_changed()

if __name__ == "__main__":
    from .EndpointRetargetingController import EndpointRetargetingController
    from ..controller import DifferentialKinematicOpenLinkageController, IKLinkageController

    ctlr = EndpointRetargetingController(
        src_model=OpenLinkage(
            link_sizes=[3.0, 1.0],
            link_angles=[0.36, 0.15],
        ),
        dest_model=OpenLinkage(
            link_sizes=[1.5, 1.5],
            link_angles=[0.36, 0.15],
        ),
        target_provider=SplineTargetProvider(),
        linkage_controller=DifferentialKinematicOpenLinkageController(max_movement=1.0, iterations=4),
    )

    driver = RetargetingDriver(
        linkage_src=ctlr.src_model,
        linkage_dest=ctlr.dest_model,
        target_provider=ctlr.target_provider,
        retargeting_controller=ctlr
    )

    driver.target_provider.button_clicked(
        mouse_x=-0.4770967741935479, mouse_y = -0.3996103896103884
    )
    driver.target_provider.button_clicked(
        mouse_x=-4.474838709677419, mouse_y = -1.8677922077922071
    )
    driver.target_provider.button_clicked(
        mouse_x=-6.926129032258065, mouse_y = -0.01324675324675173
    )
    driver.target_provider.button_clicked(
        mouse_x=-3.5041935483870965, mouse_y = 1.6536363636363651
    )

    fps = 30
    frames = np.linspace(0.0, 1.0, fps)
    from ..view.PlotAnimator import PlotAnimator

    # switch_out = False
    # if switch_out:
    #     from ..drivers.LinkageDriver import *
    #     bars = 6
    #     linkage = OpenLinkage(
    #         link_sizes=[0.5 + 2 * random.random() for i in range(bars)], 
    #         link_angles=[-math.pi / 2 + math.pi * random.random() for i in range(bars)]
    #     )
    #     path_provider = ClickTargetProvider(linkage.last_endpoint())
    #     controller = DifferentialKinematicOpenLinkageController()

    #     driver = LinkageDriver(linkage, path_provider, controller)

    animator = PlotAnimator(driver, frames=frames)
    animator.run(fps, show=False, save=True, repeat=False)

