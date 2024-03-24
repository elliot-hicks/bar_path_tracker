import gradio as gr


def add_info():
    """

    Returns
    -------
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
    """

    return (
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
    )


def submit_info():
    """
    submit_info_button,  # hide
    weight_box,  # hide
    units_drop_down,  # hide
    rpe_slider,  # hide
    exercise_box,  # hide
    bar_path_video,  # show
    speed_plot,  # show
    acceleration_plot,  # show
    distance_plot,  # show
    """

    return (
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
    )
