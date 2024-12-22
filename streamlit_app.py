import streamlit as st
from manim import *
import os
from pathlib import Path

class ThreeDCameraIllusionRotation(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        circle = Circle()
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.add(circle, axes)
        self.begin_3dillusion_camera_rotation(rate=2)
        self.wait(PI / 2)
        self.stop_3dillusion_camera_rotation()

def render_manim_scene():
    from manim import config
    from pathlib import Path

    config.media_dir = "./media"
    config.verbosity = "WARNING"

    scene = ThreeDCameraIllusionRotation()
    scene.render()

    video_dir = Path(config.media_dir) / "videos" / "1080p60"
    video_file = next(video_dir.glob("*.mp4"), None)

    if video_file is None:
        raise FileNotFoundError(f"No video file found in {video_dir}.")
    
    return str(video_file)


st.title("Manim Animation Viewer")

if st.button("Render Animation"):
    try:
        with st.spinner("Rendering animation..."):
            video_path = render_manim_scene()
        st.success("Animation rendered successfully!")
        st.video(video_path)
    except Exception as e:
        st.error(f"An error occurred: {e}")
