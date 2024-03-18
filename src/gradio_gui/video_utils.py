from typing import Tuple

import cv2
import gradio as gr
import numpy as np


def store_video(video: str) -> Tuple[str, np.ndarray, dict, dict]:
    """Store video passed to upload

    Args:
        video (str): Path to video.

    Returns:
        Tuple[str, np.ndarray, dict, dict]:
        - Video path
        - First frame
        - Update for upload video box
        - Update bounding box screen
    """
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
