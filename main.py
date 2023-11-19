import sys
import cv2
import numpy as np
import gradio as gr
from PIL import Image

from src.gradio_gui.bbox_utils import get_point, show_points, store_img, undo_points
from src.gradio_gui.video_utils import (
    store_video,
    video_selected,
    track_bar_path,
)
from src.gradio_gui.tracker_utils import track_bar_path


# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)


with gr.Blocks() as demo:
    with gr.Column():
        with gr.Row():
            original_video = gr.State(value=None)  # store original video
            first_frame = gr.State(value=None)  # store original video
            uploaded_training_video = gr.Video(
                label="Upload Training Video",
            )
            bounding_box_screen = gr.Image(
                value=None, label="Draw Bounding Box", visible=False, interactive=False
            )
            bar_path_video = gr.Video(value=None, label="Bar Path", interactive=False)
        with gr.Row():
            with gr.Column():
                # input image
                original_image = gr.State(
                    value=None
                )  # store original image without points, default None

                # basic blocks:
                input_image = gr.Image(type="numpy")
                selected_points = gr.State([])  # store points
                undo_button = gr.Button("Undo point")
                submit_button = gr.Button("Submit")

            dataframe = gr.DataFrame(
                label="Bounding Box",
                headers=["x", "y"],
                col_count=(2, "fixed"),
                datatype=["number", "number"],
            )
    # When video is uploaded:
    # return the video, first frame/ thumbnail,
    uploaded_training_video.upload(
        store_video,
        [uploaded_training_video],
        [
            original_video,
            first_frame,
            uploaded_training_video,
            bounding_box_screen,
        ],
    )

    bounding_box_screen.select(
        get_point,
        [bounding_box_screen, selected_points],
        [bounding_box_screen],
    )

    undo_button.click(
        undo_points,
        [first_frame, selected_points],
        [bounding_box_screen, selected_points],
    )

    submit_button.click(show_points, [selected_points], [dataframe])
    submit_button.click(
        track_bar_path, [uploaded_training_video, selected_points], [bar_path_video]
    )

demo.queue().launch(share=True)
