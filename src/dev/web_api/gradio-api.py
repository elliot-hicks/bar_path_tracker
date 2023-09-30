import gradio as gr
import os
import cv2

"""
import sys

sys.path.insert(0, "..")
sys.path.insert(0, "../..")

from object_tracker.object_tracker import ObjectTracker

plate_size = 0.43


def video_identity(video):
    f = cv2.VideoCapture(video)

    _, frame = f.read()
    cv2.imwrite("first_frame.jpg", frame)
    f.release()

    t = ObjectTracker()
    (
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
    ) = t.get_starting_bbox(video, plate_size=0.43)
    bar_path, video = t.track_bar_path(
        video,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        False,
    )

    return video

"""


def main():
    g = gr.Interface(
        video_identity,
        gr.Video(),
        "playable_video",
        examples=[
            r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\data\example_videos\squat_example.mp4"
        ],
        cache_examples=False,
    )

    with gr.Blocks() as demo__:
        with gr.Row():
            g.render()
            gr.Image(
                r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\Bar.png"
            )

    demo__.launch()


def image_mod(image):
    return image


def main():
    g = gr.Interface(
        image_mod,
        gr.Image(type="pil"),
        "image",
        flagging_options=["blurry", "incorrect", "other"],
        examples=[
            r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\Bar.png"
        ],
    )
    with gr.Blocks() as demo:
        with gr.Row():
            gr.Image(
                r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\Bar.png",
                tool="select",
            )

    demo.launch()


if __name__ == "__main__":
    main()
