import os
import cv2
import numpy as np
import sys
import gradio as gr

sys.path.append("src/")

from bar_path_tracker.object_tracker import ObjectTracker


def track_bar_path(video, bounding_box):
    print(bounding_box)

    f = cv2.VideoCapture(video)

    _, frame = f.read()

    print("Print Gradio shape", frame.shape)

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

    return gr.update(value=video)
