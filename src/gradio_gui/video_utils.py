import os
import cv2
import numpy as np
import gradio as gr
from PIL import Image
import sys

sys.path.append("src/")


video_examples = [
    [
        r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\src\data\example_videos\bench_example.mp4"
    ]
]


def store_video(video):
    f = cv2.VideoCapture(video)
    _, frame = f.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    f.release()

    return (
        video,
        frame,
        gr.update(visible=False),
        gr.update(visible=True, value=frame),
    )


def video_selected(video_input, first_frame):
    f = first_frame  # np.array(first_frame).squeeze()
    f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)

    return gr.update(visible=True, value=f), gr.update(
        value=track_bar_path(video_input), visible=True, scale=1
    )
