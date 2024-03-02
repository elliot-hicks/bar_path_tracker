import gradio as gr
from src.gradio_gui.bbox_utils import get_point, show_points, undo_points
from src.gradio_gui.video_utils import store_video
from src.gradio_gui.tracker_utils import track_bar_path
from src.gradio_gui.theme import Theme
from src.gradio_gui.information_utils import add_info, submit_info

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
        add_info,
        [],
        [
            bar_path_video,
            original_video,
            bounding_box_screen,
            uploaded_training_video,
            weight_box,
            units_drop_down,
            rpe_slider,
            exercise_box,
            submit_button,
            undo_button,
            submit_info_button,
        ],
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

    submit_info_button.click(
        submit_info,
        [],
        [
            submit_info_button,
            weight_box,
            units_drop_down,
            rpe_slider,
            exercise_box,
            bar_path_video,
            speed_plot,
            acceleration_plot,
            distance_plot,
        ],
    )


demo.queue().launch(share=False)
