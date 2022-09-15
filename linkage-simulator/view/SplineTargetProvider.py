import numpy as np
from scipy.interpolate import make_interp_spline

from .TargetProvider import *

MIN_SPLINE_TARGETS = 4

class SplineTargetProvider(TargetProvider):

    def __init__(self, initial_target: np.ndarray = np.array((np.inf, np.inf))) -> None:
        self._target = initial_target
        self.targets_x = []
        self.targets_y = []
        self.click_target = initial_target
        self.spline_fn = None
        self.target_trajectory: np.ndarray = np.array([(np.inf, np.inf)])
        self.src_origin = np.array((0., 0.))
        self._retarget_origins = []
        self._retarget_scales = []
        self._retarget_trajectories = []
    
    def is_valid(self):
        return self.spline_fn is not None

    def add_retargeting(self, origin: np.ndarray, scale: float):
        self._retarget_origins.append(origin)
        self._retarget_scales.append(scale)
        self._retarget_trajectories.append(self.target_trajectory * scale + origin) 

    def update_target(self, tt: float, dt: float):
        if self.spline_fn is not None:
            self._target = self.spline_fn(tt * len(self.targets_x))
    
    def button_clicked(self, mouse_x: float, mouse_y: float):
        src_x, src_y = self.src_origin
        self.targets_x.append(mouse_x - src_x)
        self.targets_y.append(mouse_y - src_y)
        self.click_target = np.array((mouse_x, mouse_y))

        if len(self.targets_x) >= MIN_SPLINE_TARGETS:
            PATH_SMOOTHNESS = 5
            
            splinefn_xs = self.targets_x + self.targets_x[0:2]
            splinefn_ys = self.targets_y + self.targets_y[0:2]
            self.spline_fn = make_interp_spline(
                list(range(len(splinefn_xs))),
                np.c_[splinefn_xs, splinefn_ys]
            )

            splinefn_x = \
                np.linspace(0, len(self.targets_x), len(self.targets_x) * PATH_SMOOTHNESS)
            xys = self.spline_fn(splinefn_x) \
                    if self.spline_fn is not None\
                    else np.array([[0, 0]])
            self.target_trajectory = xys + self.src_origin
            for i in range(len(self._retarget_origins)):
                self._retarget_trajectories[i] = xys * self._retarget_scales[i] + self._retarget_origins[i]

    def get_full_trajectory(self):
        return self.target_trajectory
    
    def draw(self, ax: matplotlib.axes.Axes, lines: Tuple[matplotlib.lines.Line2D] = None, offset: Tuple[float, float] = (0.0, 0.0)) -> Tuple[matplotlib.lines.Line2D]:

        x_verts = self.targets_x + [self._target[0]]
        y_verts = self.targets_y + [self._target[1]]
        x_verts = np.array(x_verts) + offset[0] + self.src_origin[0]
        y_verts = np.array(y_verts) + offset[1] + self.src_origin[1]

        artists = lines if lines is not None else []

        if lines is None or len(lines) == 0:
            target_dots = ax.scatter(x_verts, y_verts)
        else:
            target_dots = lines[0]
            target_dots.set_offsets(np.array(list(zip(x_verts, y_verts))))
        artists.append(target_dots)


        xys = self.target_trajectory + offset
        if lines is None or len(lines) < 2:
            spline_line = ax.plot(xys[:, 0], xys[:, 1])[0]
        else:
            spline_line = lines[1]
            spline_line.set_data(xys[:, 0], xys[:, 1])
        artists.append(spline_line)

        for retarget_index, retarget_xyz in enumerate(self._retarget_trajectories):
            if lines is None or len(lines) < (3 + retarget_index):
                retarget_line = ax.plot(retarget_xyz[:, 0], retarget_xyz[:, 1])[0]
            else:
                retarget_line = lines[2 + retarget_index]
                retarget_line.set_data(retarget_xyz[:, 0], retarget_xyz[:, 1])
            artists.append(retarget_line)

        return artists

    @property
    def target(self) -> np.ndarray:
        return self._target

    def dest_target(self, dest_index: int) -> np.ndarray:
        # Don't offset! The offset is for drawing only!
        return self.target * self._retarget_scales[dest_index] # + self._retarget_origins[i]