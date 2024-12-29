# from __future__ import annotations
import math
from manim import *
import numpy as np
from typing import Iterable
from sympy.solvers import solve
from sympy import Symbol

ROTATION_X_AXIS = 0
ROTATION_Y_AXIS = 1

lower_bound = 0
upper_bound = math.pi
rotation = ROTATION_Y_AXIS

f = lambda x: math.sin(3*x)

# def f_inverse(x):
#     y = Symbol('y')
#     sols = solve(y**2 - x, y)
#     print(f"solved: {sols}")
#     return sols[0]


# custom implementation of get_area function but for area between function and y axis
# based on:
# https://github.com/ManimCommunity/manim/blob/2275ec5916de0ad3bedbc276da09fc3bfbae4d5e/manim/mobject/coordinate_systems.py#L1183
# def get_area_to_y_axis(
#         self,
#         graph: ParametricFunction,
#         y_range: tuple[float, float] | None = None,
#         color: ManimColor | Iterable[ManimColor] = [BLUE, GREEN],
#         opacity: float = 0.3,
#         bounded_graph: ParametricFunction = None,
#         **kwargs,
#     ):

#     if y_range is None:
#         a = graph.t_min
#         b = graph.t_max
#     else:
#         a, b = y_range

#     if bounded_graph is None:
#         points = (
#             [self.c2p(a), graph.function(a)]
#             + [p for p in graph.points if a <= self.p2c(p)[0] <= b]
#             + [graph.function(b), self.c2p(b)]
#         )

#     return Polygon(*points, **kwargs).set_opacity(opacity).set_color(color)


class FunctionAnimation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-8, 8, 2],
            y_range=[-8, 8, 2],
            z_range=[-6, 6, 2],
            x_length=16,
            y_length=16,
            z_length=12,
            axis_config={"include_numbers": True},
            z_axis_config={"include_numbers": True},
        )

        axes_label = axes.get_axis_labels(x_label="x", y_label="f(x)", z_label=None) 


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
            # curve_args["y_range"] = [lower_bound, upper_bound]
            curve_args["x_range"] = [lower_bound, upper_bound]


        curve = axes.plot(**curve_args)


        area_args = {
            "graph": curve,
            "color": ORANGE,
        }

        if rotation == ROTATION_X_AXIS:
            area_args["x_range"] = [lower_bound, upper_bound]
        else:
            # error
            # area_args["y_range"] = [lower_bound, upper_bound]
            area_args["x_range"] = [lower_bound, upper_bound]

        # does not work with ImplicitFunction
        if rotation == ROTATION_X_AXIS:
            area = axes.get_area(**area_args)
        else:
            area = Polygon(
                    [lower_bound, f(lower_bound), 0],
                    [0, f(upper_bound), 0],
                    [upper_bound, f(upper_bound), 0],
                    [upper_bound, 0, 0],
                    color=GREEN,
                    fill_color=GREEN,
                    fill_opacity=1
                )
            # area = Difference(Polygon(
            #         [lower_bound, f(lower_bound), 0],
            #         [0, f(upper_bound), 0],
            #         [upper_bound, f(upper_bound), 0],
            #         [upper_bound, 0, 0],
            #         color=GREEN,
            #         fill_color=GREEN,
            #         fill_opacity=1
            #     ), axes.get_area(**area_args))
        

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
        self.add(axes, axes_label)
        self.play(Create(curve), FadeIn(area))
        self.wait()
        # theta -40 deg for rotation around x axis
        # theta 40 deg for rotation around y axis
        self.move_camera(
            phi=60 * DEGREES,
            theta=-40 * DEGREES if rotation == ROTATION_X_AXIS else 40 * DEGREES,
            zoom=0.75
        )

        self.begin_ambient_camera_rotation(rate=PI/2)

        self.play(
            Create(
                surface,
                lag_ratio=0.8,
                run_time=1
            ),
            Rotate(
                rotation_group,
                angle=2*PI if rotation == ROTATION_X_AXIS else -2*PI,
                axis=RIGHT if rotation == ROTATION_X_AXIS else UP,
                about_point=axes.c2p(0,0,0),
                run_time=1
            )
        )

        self.wait(4)
        
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
        self.stop_ambient_camera_rotation()
        self.wait()

        # self.begin_3dillusion_camera_rotation(rate=2)
        # self.wait(1.5)
        # self.stop_3dillusion_camera_rotation()

