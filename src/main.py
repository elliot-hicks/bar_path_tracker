import sys
import gradio as gr
from gradio_gui.bbox_utils import get_point, undo_points
from gradio_gui.video_utils import store_video
from gradio_gui.tracker_utils import track_bar_path
from gradio_gui.theme import Theme
from gradio_gui.information_utils import add_info, submit_info

sys.path.append(".")

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
                    weight_box = gr.Textbox(
                        value="",
                        label="Weight",
                        info="Insert the weight used",
                        visible=False,
                        interactive=True,
                    )
                    units_drop_down = gr.Dropdown(
                        ["kg", "lb"],
                        multiselect=False,
                        interactive=True,
                        visible=False,
                        value="kg",
                        info="Select unit of weight",
                    )
                rpe_slider = gr.Slider(
                    0,
                    10,
                    step=0.5,
                    value="",
                    label="RPE",
                    info="Insert the RPE",
                    visible=False,
                    interactive=True,
                )
                exercise_box = gr.Dropdown(
                    ["Squat", "Bench", "Deadlift"],
                    label="Exercise",
                    info="Insert the exercise for tracking",
                    visible=False,
                    interactive=True,
                )
                with gr.Row():
                    undo_button = gr.Button("Undo point")
                    submit_button = gr.Button("Submit Bounding Box")
                    submit_info_button = gr.Button("Submit Data", visible=False)

            with gr.Tab("Distance"):
                distance_plot = gr.Plot(visible=False)
            with gr.Tab("Speed"):
                speed_plot = gr.Plot(visible=False)
            with gr.Tab("Acceleration"):
                acceleration_plot = gr.Plot(visible=False)

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

    # Select points for bounding box:
    bounding_box_screen.select(
        get_point,
        [bounding_box_screen, selected_points],
        [bounding_box_screen],
    )

    # Undo a chosen corner of the bounding box:
    undo_button.click(
        undo_points,
        [first_frame, selected_points],
        [bounding_box_screen, selected_points],
    )

    # Submit button for bounding box:
    submit_button.click(
        add_info,
        [],
        [
            bar_path_video,  # hide
            original_video,  # hide
            bounding_box_screen,  # hide
            uploaded_training_video,  # hide
            weight_box,  # show
            units_drop_down,  # show
            rpe_slider,  # show
            exercise_box,  # show
            submit_button,  # hide
            undo_button,  # hide
            submit_info_button,  # show
        ],
    )

    submit_button.click(
        track_bar_path,
        [uploaded_training_video, selected_points],
        [
            bounding_box_screen,  # update value
            bar_path_video,  # update value
            speed_plot,  # update value
            acceleration_plot,  # update value
            distance_plot,  # update value
        ],
    )

    submit_info_button.click(
        submit_info,
        [],
        [
            submit_info_button,  # hide
            weight_box,  # hide
            units_drop_down,  # hide
            rpe_slider,  # hide
            exercise_box,  # hide
            bar_path_video,  # show
            speed_plot,  # show
            acceleration_plot,  # show
            distance_plot,  # show
        ],
    )


demo.queue().launch(share=False)
