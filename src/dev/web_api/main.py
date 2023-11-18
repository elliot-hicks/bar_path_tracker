import os
import cv2
import numpy as np
import gradio as gr
from PIL import Image


from bbox_utils import get_point, show_points, store_img, undo_points


# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)

with gr.Blocks() as demo:
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

    input_image.upload(store_img, [input_image], [original_image, selected_points])

    input_image.select(
        get_point,
        [input_image, selected_points],
        [input_image],
    )

    undo_button.click(
        undo_points, [original_image, selected_points], [input_image, selected_points]
    )

    submit_button.click(show_points, [selected_points], [dataframe])

demo.queue().launch()
