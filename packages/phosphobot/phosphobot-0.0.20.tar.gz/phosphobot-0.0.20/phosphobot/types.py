from typing import Literal
from enum import Enum


VideoCodecs = Literal[
    "avc1",
    "hev1",
    "mp4v",
    "hvc1",
    "avc3",
    "av01",
    "vp09",
]

CameraTypes = Literal[
    "classic",
    "stereo",
    "realsense",
    "realsense_rgb",
    "realsense_depth",
    "dummy",
    "dummy_stereo",
    "unknown",
]


class SimulationMode(str, Enum):
    headless = "headless"
    gui = "gui"


class VideoCodecsEnum(str, Enum):
    # Typer doesn't support Literal, so we use an Enum instead
    # Virtually the same as phosphobot.models.VideoCodecs
    avc1 = "avc1"
    hev1 = "hev1"
    mp4v = "mp4v"
    hvc1 = "hvc1"
    avc3 = "avc3"
    av01 = "av01"
    vp09 = "vp09"
