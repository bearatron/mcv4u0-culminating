import math
from manim import *
import numpy as np

ROTATION_X_AXIS = 0
ROTATION_Y_AXIS = 1

lower_bound = -1.5
upper_bound = 1.5
rotation = ROTATION_X_AXIS

def f(x):
    return x**3


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

        # curve = ImplicitFunction(
        #     func=lambda x, y: f(x) - y,
        #     x_range=[lower_bound, upper_bound],
        # )

        curve_args = {
            "function": lambda x: f(x),
            "color": ORANGE,
        }

        if rotation == ROTATION_X_AXIS:
            curve_args["x_range"] = [lower_bound, upper_bound]
        else:
            # no y_range argument so this throws an error
            curve_args["y_range"] = [lower_bound, upper_bound]

        curve = axes.plot(**curve_args)


        area_args = {
            "graph": curve,
            "color": ORANGE,
        }

        if rotation == ROTATION_X_AXIS:
            area_args["x_range"] = [lower_bound, upper_bound]
        else:
            area_args["y_range"] = [lower_bound, upper_bound]

        # does not work with ImplicitFunction
        area = axes.get_area(**area_args)

        rotation_group = VGroup(curve, area)


        surface_args = {
            "u_range": [0, 2*PI],
            "v_range": [lower_bound, upper_bound],
            "checkerboard_colors": [BLUE_B, BLUE_D],
        }

        if rotation == ROTATION_X_AXIS:
            surface_args["func"] = lambda u, v: axes.c2p(
                v,
                f(v) * np.cos(u),
                f(v) * np.sin(u),
            )
        else: 
            surface_args["func"] = lambda u, v: axes.c2p(
                v * np.cos(u),
                f(v),
                v * np.sin(u),
            )


        surface = Surface(**surface_args)

        # surface = Surface(
        #     lambda u, v: axes.c2p(
        #         v * np.cos(u),
        #         f(v),
        #         v * np.sin(u),
        #     ),
        #     u_range=[0, 2*PI],
        #     v_range=[0, upper_bound],
        #     checkerboard_colors=[BLUE_B, BLUE_D],
        # )

        # surface = Surface(
        #     lambda u, v: axes.c2p(
        #         v,
        #         f(v) * np.cos(u),
        #         f(v) * np.sin(u),
        #     ),
        #     u_range=[0, 2*PI],
        #     v_range=[lower_bound, upper_bound],
        #     checkerboard_colors=[BLUE_B, BLUE_D],
        # )

        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes)
        self.play(Create(curve), FadeIn(area))
        self.wait()
        # theta -40 deg for rotation around x axis
        # theta 40 deg for rotation around y axis
        self.move_camera(phi=60 * DEGREES, theta=-40 * DEGREES, zoom=0.5)

        # self.begin_ambient_camera_rotation(rate=PI/10)
        self.play(
            Create(
                surface,
                lag_ratio=0.8,
                run_time=1
            ),
            Rotate(
                rotation_group,
                angle=2 * PI,
                axis=RIGHT,
                about_point=axes.c2p(0,0,0),
                run_time=1
            )
        )
        # self.play(
        #     Create(
        #         surface,
        #         lag_ratio=0.8,
        #         run_time=1
        #     ),
        #     Rotate(
        #         curve,
        #         angle=-2 * PI, # rotation towards the left to match surface
        #         axis=UP,
        #         about_point=axes.c2p(0,0,0),
        #         run_time=1
        #     )
        # )
        # self.stop_ambient_camera_rotation()
        self.wait()

        # self.begin_3dillusion_camera_rotation(rate=2)
        # self.wait(1.5)
        # self.stop_3dillusion_camera_rotation()

