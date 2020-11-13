
from .TargetProvider import *

class ClickTargetProvider(TargetProvider):

    def __init__(self, initial_target: Point2d = (0, 0)) -> None:
        self._target = initial_target
        self.click_target = initial_target
    
    def update_target(self, tt: float, dt: float):
        
        self._target = TargetProvider.interpolate(self._target, self.click_target, 0.1)
    
    def button_clicked(self, mouse_x: float, mouse_y: float):
        self.click_target = (mouse_x, mouse_y)

    @property
    def target(self) -> Point2d:
        return self._target