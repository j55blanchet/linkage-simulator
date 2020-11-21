from matplotlib.lines import Line2D
from typing import Tuple

from .model import *
from .controller import *
from .view import *

class LinkageDriver:
    def __init__(self, linkage: Linkage, target_provider: TargetProvider, controller: LinkageController) -> None:
        self.linkage = linkage
        self.controller = controller
        self.ln_linkage = None
        self.ln_target = None
        self.target_provider = target_provider
        self.pframe = 0

    def get_plot_size(self) -> Tuple[float, float, float, float]:
        return self.linkage.get_plot_bounds()

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

    