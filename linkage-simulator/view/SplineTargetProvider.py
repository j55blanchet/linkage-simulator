import numpy as np
from scipy.interpolate import make_interp_spline

from .TargetProvider import *

MIN_SPLINE_TARGETS = 4

class SplineTargetProvider(TargetProvider):

    def __init__(self, initial_target: np.array = np.array((np.inf, np.inf))) -> None:
        self._target = initial_target
        self.targets_x = []
        self.targets_y = []
        self.click_target = initial_target
        self.spline_fn = None
    
    def update_target(self, tt: float, dt: float):

        if self.spline_fn is not None:
            self._target = self.spline_fn(tt * len(self.targets_x))
    
    def button_clicked(self, mouse_x: float, mouse_y: float):
        self.targets_x.append(mouse_x)
        self.targets_y.append(mouse_y)
        self.click_target = np.array((mouse_x, mouse_y))

        if len(self.targets_x) >= MIN_SPLINE_TARGETS:

            splinefn_xs = self.targets_x + self.targets_x[0:2]
            splinefn_ys = self.targets_y + self.targets_y[0:2]
            self.spline_fn = make_interp_spline(
                list(range(len(splinefn_xs))),
                np.c_[splinefn_xs, splinefn_ys]
            )

    
    def draw(self, ax: matplotlib.axes.Axes, lines: Tuple[matplotlib.lines.Line2D] = None, offset: Tuple[float, float] = (0.0, 0.0)) -> Tuple[matplotlib.lines.Line2D]:

        x_verts = self.targets_x + [self._target[0]]
        y_verts = self.targets_y + [self._target[1]]
        x_verts = np.array(x_verts) + offset[0]
        y_verts = np.array(y_verts) + offset[1]

        artists = lines if lines is not None else []

        if lines is None or len(lines) == 0:
            target_dots = ax.scatter(x_verts, y_verts)
        else:
            target_dots = lines[0]
            target_dots.set_offsets(np.array(list(zip(x_verts, y_verts))))
        artists.append(target_dots)


        splinefn_x = np.linspace(0, len(self.targets_x), len(self.targets_x) * 20)
        xys = self.spline_fn(splinefn_x) \
                    if self.spline_fn is not None\
                    else np.array([[0, 0]])
        xys = xys + offset
        if lines is None or len(lines) < 2:
            spline_line = ax.plot(xys[:, 0], xys[:, 1])[0]
        else:
            spline_line = lines[1]
            spline_line.set_data(xys[:, 0], xys[:, 1])
        artists.append(spline_line)

        return artists

    @property
    def target(self) -> np.array:
        return self._target