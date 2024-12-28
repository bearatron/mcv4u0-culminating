import math
from manim import *
import numpy as np


class FunctionAnimation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-6, 6 , 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=8,
            y_length=6,
            z_length=6,
        )
        circle = Circle()
        graph = ImplicitFunction(
            lambda x, y: x**2- y,
        )

        surface = Surface(
            lambda u, v: axes.c2p(v * np.cos(u), v * np.sin(u), 0.5 * v ** 2),
            u_range=[0, 2*PI],
            v_range=[0, 3],
            checkerboard_colors=[GREEN, RED],
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-40 * DEGREES)
        self.add(axes, graph, surface)
        self.begin_ambient_camera_rotation(rate=PI/10)
        self.play(
            Rotate(
                graph,
                angle=2 * PI,
                axis=UP,
                about_point=axes.c2p(0,0,0),
            )
        )
        self.stop_ambient_camera_rotation()

        # self.begin_3dillusion_camera_rotation(rate=2)
        # self.wait(1.5)
        # self.stop_3dillusion_camera_rotation() 