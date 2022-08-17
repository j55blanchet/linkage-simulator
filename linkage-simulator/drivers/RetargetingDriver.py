from typing import *

from matplotlib.lines import Line2D

from ..model.OpenLinkage import OpenLinkage
from .DriverBase import DriverBase


class RetargetingDriver(DriverBase):

    def __init__(self, linkage_src: OpenLinkage, linkage_dest: OpenLinkage) -> None:
        self.linkage_src = linkage_src
        self.linkage_dest = linkage_dest

        self.plot_size = self.get_plot_size()
        self.origin_src = -self.plot_size[0] / 2, 0.0 # 25% x, center y
        self.origin_dest = self.plot_size[0] / 2, 0.0 # 75% x, center y
        
        self.ln_linkage_src = None
        self.ln_linkage_dest = None

    def get_plot_size(self) -> Tuple[float, float, float, float]:
        sx_min, sx_max, sy_min, sy_max = self.linkage_src.get_plot_bounds()
        dx_min, dx_max, dy_min, dy_max = self.linkage_dest.get_plot_bounds()

        # plot the two charts side by side
        half_width = max(sx_max, dx_max) - min(sx_min, dx_min)
        height = max(sy_max, dy_max) - min(sy_min, dy_min)
        return -half_width, half_width, -height/2, height/2

    def update(self, frame: float):
        pass
    
    def plot(self, ax) -> Tuple[Line2D]:
        self.ln_linkage_src = self.linkage_src.draw(ax, self.ln_linkage_src, offset=self.origin_src)
        self.ln_linkage_dest = self.linkage_dest.draw(ax, self.ln_linkage_dest, offset=self.origin_dest)
        return (*self.ln_linkage_src, *self.ln_linkage_dest)
    

if __name__ == "__main__":
    


    driver = RetargetingDriver(
        linkage_src=OpenLinkage(
            link_sizes=[3.0, 1.0],
            link_angles=[0.15, 0.36],
        ),
        linkage_dest=OpenLinkage(
            link_sizes=[1.5, 1.5],
            link_angles=[0.15, 0.36],
        ),
    )
    from ..view.PlotAnimator import PlotAnimator
    animator = PlotAnimator(driver)
    animator.run()

