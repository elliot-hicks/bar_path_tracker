import os
import cv2
import numpy as np
import gradio as gr
from PIL import Image

from bar_path_tracker.object_tracker import ObjectTracker

plate_size = 0.43


def track(video):
    """
    f = cv2.VideoCapture(video)

    _, frame = f.read()

    t = ObjectTracker()

    starting_bbox = [100, 200, 300, 400]
    starting_bbox_centre = [250, 250]
    meters_per_pixel = 0.4

    bar_path, video = t.track_bar_path(
        video,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        False,
    )

    print(video)
    """

    path = r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\src\data\results\CSRT_with_stats.mp4"

    return path


# points color and marker
colors = [(255, 0, 0), (0, 255, 0)]
markers = [1, 5]

# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)
image_examples = [
    [
        r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\bar_path_logo.png"
    ],
]
# video examples
video_examples = [
    [
        r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\src\data\example_videos\bench_example.mp4"
    ]
]


def store_video(video):
    f = cv2.VideoCapture(video)
    _, frame = f.read()
    f.release()

    return video, frame


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
                markerType=markers[1],
                markerSize=20,
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
def undo_points(orig_img, sel_pix, first_frame):
    temp = first_frame.squeeze()
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)

    # draw points
    if len(sel_pix) != 0:
        sel_pix.pop()
        for point in sel_pix:
            cv2.drawMarker(
                temp,
                point,
                colors[1],
                markerType=markers[1],
                markerSize=20,
                thickness=5,
            )

    return temp if isinstance(temp, np.ndarray) else np.array(temp)


def video_selected(video_input, first_frame):
    f = first_frame  # np.array(first_frame).squeeze()
    f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)

    return gr.update(visible=True, value=f), gr.update(
        value=track(video_input), visible=True, scale=1
    )


def hide_image():
    return gr.update(visible=False)


with gr.Blocks() as demo:
    with gr.Tab(
        "Upload",
    ):
        with gr.Row():
            original_video = gr.State(value=None)  # store original video
            first_frame = gr.State(value=None)  # store original video
            input_video = gr.Video(label="Video", size=(100, 200))

            with gr.Column():
                # input image
                original_image = gr.State(
                    value=None
                )  # store original image without points, default None

                input_image = gr.Image(
                    type="numpy", value=image_examples[0][0], visible=False, scale=1
                )

                selected_points = gr.State([])  # store points
                bbox_hint = gr.Markdown(
                    "You can click on the image to select points prompt. Default: foreground_point."
                )
                undo_button = gr.Button("Undo point")
                submit_button = gr.Button("Submit")

            output_video = gr.Video(label="Bar Path", visible=False)

    input_video.upload(store_video, [input_video], [original_video, first_frame])
    input_video.change(
        fn=video_selected,
        inputs=[input_video, first_frame],
        outputs=[input_image, output_video],
    )

    input_image.select(
        get_point,
        [input_image, selected_points],
        [input_image],
    )

    undo_button.click(
        undo_points, [original_image, selected_points, first_frame], [input_image]
    )
    submit_button.click(
        hide_image,
        inputs=None,
        outputs=None,
    )

demo.queue().launch(debug=True, enable_queue=True, height=1000)
