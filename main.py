import gradio as gr
from src.gradio_gui.bbox_utils import get_point, show_points, undo_points
from src.gradio_gui.video_utils import store_video
from src.gradio_gui.tracker_utils import track_bar_path
from src.gradio_gui.theme import Theme

# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)

custom_theme = Theme()

with gr.Blocks(theme=custom_theme) as demo:
    with gr.Column():
        with gr.Row(equal_height=True):
            with gr.Column():
                original_video = gr.State(
                    value=None, height="50vw"
                )  # store original video
                first_frame = gr.State(
                    value=None, height="50vw"
                )  # store original video
                bar_path_stats = gr.State(value=None, height="50vw")
                uploaded_training_video = gr.Video(
                    label="Upload Training Video", height="50vw"
                )
                selected_points = gr.State([])  # store points
                bounding_box_screen = gr.Image(
                    value=None,
                    label="Draw Bounding Box",
                    visible=False,
                    interactive=False,
                    type="numpy",
                    height="50vw",
                )
                bar_path_video = gr.Video(
                    value=None,
                    label="Bar Path",
                    interactive=False,
                    visible=False,
                    height="50vw",
                )
                with gr.Row():
                    undo_button = gr.Button("Undo point")
                    submit_button = gr.Button("Submit")

            with gr.Tab("Distance"):
                distance_plot = gr.Plot()
            with gr.Tab("Speed"):
                speed_plot = gr.Plot()
            with gr.Tab("Acceleration"):
                acceleration_plot = gr.Plot()

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

    submit_button.click(
        track_bar_path,
        [uploaded_training_video, selected_points],
        [
            bounding_box_screen,
            bar_path_video,
            speed_plot,
            acceleration_plot,
            distance_plot,
        ],
    )


demo.queue().launch(share=False)
