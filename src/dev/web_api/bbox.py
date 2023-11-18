import os
import cv2
import numpy as np
import gradio as gr
from PIL import Image

"""
import sys

sys.path.insert(0, "..")
sys.path.insert(0, "../../..")

from object_tracker.object_tracker import ObjectTracker

plate_size = 0.43


def track(video):
    f = cv2.VideoCapture(video)

    _, frame = f.read()

    t = ObjectTracker()

    starting_bbox = None
    starting_bbox_centre = None
    meters_per_pixel = None

    bar_path, video = t.track_bar_path(
        video,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        False,
    )

    return video

"""

# points color and marker
colors = [(255, 0, 0), (0, 255, 0)]
markers = [1, 5]

# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)
image_examples = [
    [r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\Bar.png"],
    [
        r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\bar_path_tiled.jpg"
    ],
]


# once user upload an image, the original image is stored in `original_image`
def store_img(img):
    return img, []  # when new image is uploaded, `selected_points` should be empty


# user click the image to get points, and show the points on the image
def get_point(img, sel_pix, evt: gr.SelectData):
    if len(sel_pix) < 2:
        sel_pix.append(evt.index)  # append the background_point

        # draw points
        for point in sel_pix:
            cv2.drawMarker(
                img,
                point,
                colors[1],
                markerType=markers[0],
                markerSize=0,
                thickness=5,
            )

        if len(sel_pix) == 2:
            start_point = sel_pix[0]
            end_point = sel_pix[1]
            color = (255, 0, 0)
            thickness = 2
            cv2.rectangle(img, start_point, end_point, color, thickness)
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img if isinstance(img, np.ndarray) else np.array(img)


# undo the selected point
def undo_points(orig_img, sel_pix):
    temp = orig_img.copy()

    print(temp.shape)

    # draw points
    if len(sel_pix) != 0:
        sel_pix.pop()
        for point in sel_pix:
            cv2.drawMarker(
                temp,
                point,
                colors[1],
                markerType=markers[0],
                markerSize=00,
                thickness=5,
            )

    return temp if isinstance(temp, np.ndarray) else np.array(temp), sel_pix


def show_points(selected_points):
    return gr.update(value=selected_points)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            # input image
            original_image = gr.State(
                value=None
            )  # store original image without points, default None

            input_image = gr.Image(type="numpy")

            selected_points = gr.State([])  # store points
            bbox_hint = gr.Markdown(
                "You can click on the image to select points prompt. Default: foreground_point."
            )
            undo_button = gr.Button("Undo point")
            submit_button = gr.Button("Submit")

        dataframe = gr.DataFrame(
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

    print(selected_points)

    submit_button.click(show_points, [selected_points], [dataframe])

demo.queue().launch()
