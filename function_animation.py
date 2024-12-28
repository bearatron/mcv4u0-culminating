import math
from manim import *
import numpy as np

left_bound = -2
right_bound = 2

def f(x):
    return x**2


class FunctionAnimation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            z_range=[-10, 10, 2],
            x_length=20,
            y_length=20,
            z_length=20,
        ).add_coordinates()

        graph = ImplicitFunction(
            func=lambda x, y: f(x) - y,
            x_range=[left_bound, right_bound],
        )

        # area = axes.get_area(graph=graph, x_range=)

        surface = Surface(
            lambda u, v: axes.c2p(
                v * np.cos(u),
                f(v),
                v * np.sin(u),
            ),
            u_range=[0, 2*PI],
            v_range=[0, right_bound],
            checkerboard_colors=[BLUE_B, BLUE_D],
        )

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes)
        self.play(Create(graph))
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=-40 * DEGREES)

        self.begin_ambient_camera_rotation(rate=PI/10)
        self.play(
            Create(surface),
            Rotate(
                graph,
                angle=2 * PI,
                axis=UP,
                about_point=axes.c2p(0,0,0),
            )
        )
        self.stop_ambient_camera_rotation()

        self.wait()

        # self.begin_3dillusion_camera_rotation(rate=2)
        # self.wait(1.5)
        # self.stop_3dillusion_camera_rotation()

