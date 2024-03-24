import sys
from typing import Tuple

import gradio as gr
import numpy as np
import pandas as pd

from gradio_gui.plot_utils import (
    return_distance_plot,
    return_speed_plot,
    return_max_acceleration_bar_plot,
    return_max_speed_bar_plot,
)

colors = [(5, 150, 105), (5, 150, 105)]

sys.path.append("src/")

from bar_path_tracker.object_tracker import ObjectTracker


def track_bar_path(
    video: str, bounding_box: np.ndarray
) -> Tuple[dict, dict, dict, dict, dict]:
    """Given a video path and initial weight bounding box,
    track a bar path.

    Parameters
    ----------
    video : str
        Path to video for tracking / analysis
    bounding_box : np.ndarray
        Initial bounding box for starting weight position.

    Returns
    -------
    Tuple[dict, dict, dict, dict, dict]
        Gradio updates:
        - hide bounding box screen
        - update bar path video
        - update speed plot
        - update acceleration plot
        - update distance plot
    """
    meters_per_pixel = {}

    # Set up object tracker:
    tracker = ObjectTracker()

    bounding_box = np.array(bounding_box).flatten()

    starting_bbox_centre = [
        int((bounding_box[0] + bounding_box[2]) / 2),
        int((bounding_box[1] + bounding_box[3]) / 2),
    ]
    top_left = bounding_box[0], bounding_box[1]
    width = bounding_box[2] - bounding_box[0]
    height = bounding_box[3] - bounding_box[1]

    starting_bbox = [top_left[0], top_left[1], width, height]

    # approximate meters per pixel
    meters_per_pixel["y"] = 0.45 / height
    meters_per_pixel["x"] = 0.45 / width

    # analyse video:
    bar_path, video = tracker.track_bar_path(
        video,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        False,
    )

    # Get stats and reps:
    stats, reps = tracker.get_set_summary(bar_path, 70)

    # stats: {time: {'speeds', 'accelerations', 'x_distance','y_distance'}}
    # reps:  {1: {'frame_inds': [0, 150], 'times': [0.033, 5.037]}
    data_frame = stats_to_pd_dataframe(stats, reps)
    speed_plot = return_speed_plot(data_frame)
    max_speed_plot = return_max_speed_bar_plot(data_frame)
    max_acceleration_plot = return_max_acceleration_bar_plot(data_frame)
    distance_plot = return_distance_plot(data_frame)

    return (
        gr.update(visible=False),
        gr.update(value=video),
        gr.update(value=speed_plot),
        gr.update(value=max_speed_plot),
        gr.update(value=max_acceleration_plot),
        gr.update(value=distance_plot),
    )


def stats_to_pd_dataframe(
    stats: dict[float, dict[str, float]], rep_stats: dict[str, dict[str, int]]
) -> pd.DataFrame:
    """Convert dictionaries of stats into a pandas DataFrame for ease of
    reading.

    Parameters
    ----------
    stats : dict[float, dict[str, float]]
        Dictionary {time: {metric: metric_value}}
    rep_stats : dict[str, dict[str, int]]
        Dictionary {"rep": {"rep_inds": index, "rep_times": time}}

    Returns
    -------
    pd.DataFrame
        Dataset with columns:
        - "rep",
        - "time",
        - "x_distance",
        - "y_distance",
        - "speed",
        - "acceleration"
    """
    times = list(stats.keys())
    speeds = []
    accelerations = []
    x_distances = []
    y_distances = []

    for t in times:
        speeds.append(stats[t]["speeds"])
        accelerations.append(stats[t]["accelerations"])
        x_distances.append(stats[t]["x_distance"])
        y_distances.append(stats[t]["y_distance"])

    reps = [0] * len(times)
    reps = np.array(reps)

    for rep, rep_times in rep_stats.items():
        rep_frame_inds = rep_times["frame_inds"]
        reps[rep_frame_inds[0] : rep_frame_inds[1]] = int(rep)

    data = list(zip(reps, times, x_distances, y_distances, speeds, accelerations))
    labels = ["rep", "time", "x_distance", "y_distance", "speed", "acceleration"]

    data = pd.DataFrame(data, columns=labels)

    return data
