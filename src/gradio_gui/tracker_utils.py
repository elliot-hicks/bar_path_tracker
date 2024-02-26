import os
import cv2
import numpy as np
import sys
import pandas as pd
import gradio as gr
from src.gradio_gui.plot_utils import (
    return_acceleration_plot,
    return_speed_plot,
    return_bar_plot,
    return_distance_plot,
)

sys.path.append("src/")

from bar_path_tracker.object_tracker import ObjectTracker


def track_bar_path(video, bounding_box):

    f = cv2.VideoCapture(video)

    _, frame = f.read()

    t = ObjectTracker()

    bounding_box = np.array(bounding_box).flatten()

    starting_bbox_centre = [
        int((bounding_box[0] + bounding_box[2]) / 2),
        int((bounding_box[1] + bounding_box[3]) / 2),
    ]
    top_left = bounding_box[0], bounding_box[1]
    width = bounding_box[2] - bounding_box[0]
    height = bounding_box[3] - bounding_box[1]

    starting_bbox = [top_left[0], top_left[1], width, height]

    meters_per_pixel = 0.4

    bar_path, video = t.track_bar_path(
        video,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        False,
    )

    stats, reps = t.get_set_summary(bar_path, 70)

    # stats: {time: {'speeds', 'accelerations', 'x_distance','y_distance'}}
    # reps:  {1: {'frame_inds': [0, 150], 'times': [0.033, 5.037]}
    dataframe = stats_to_pd_dataframe(stats, reps)
    speed_plot = return_speed_plot(dataframe)
    acceleration_plot = return_bar_plot(dataframe)
    distance_plot = return_distance_plot(dataframe)

    return (
        gr.update(visible=False),
        gr.update(value=video, visible=True),
        gr.update(value=speed_plot),
        gr.update(value=acceleration_plot),
        gr.update(value=distance_plot),
    )


def stats_to_pd_dataframe(stats, rep_stats):
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
