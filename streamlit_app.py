import streamlit as st
import os
from pathlib import Path
import subprocess

subprocess.run(["echo", "helloworld"], check=True, capture_output=True)
subprocess.run(["sudo", "-l"], check=True, capture_output=True)

subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
subprocess.run(["sudo", "apt", "install",
                "build-essential", "python3-dev",
                "libcairo2-dev", "libpango1.0-dev", "ffmpeg"], check=True, capture_output=True)
subprocess.run(["pip3", "install", "manim"], check=True, capture_output=True)

try:
    import manim
except ImportError:
    st.write("bruh")


def run_shell_command(command):
    """Run a shell command and return the output."""
    try:
        result = subprocess.run(command, shell=True,
                                text=True, capture_output=True)
        if result.returncode == 0:
            return f"Command succeeded:\n{result.stdout}"
        else:
            return f"Command failed:\n{result.stderr}"
    except Exception as e:
        return f"Error while running command: {e}"


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

# run_shell_command("sudo apt update")
# run_shell_command("sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev ffmpeg")


st.set_page_config(
    page_title='Volume Visualizer',
    page_icon=':bar_chart:'
)

st.title("Manim Animation Viewer")

if st.button("Render Animation"):
    try:
        with st.spinner("Rendering animation..."):
            video_path = render_manim_scene()
        st.success("Animation rendered successfully!")
        st.video(video_path)
    except Exception as e:
        st.error(f"An error occurred: {e}")
