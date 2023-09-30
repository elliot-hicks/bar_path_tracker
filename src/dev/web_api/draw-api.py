import os
import cv2
import numpy as np
import gradio as gr


# points color and marker
colors = [(255, 0, 0), (0, 255, 0)]
markers = [1, 5]

# image examples
# in each list, the first element is image path,
# the second is id (used for original_image State),
# the third is an empty list (used for selected_points State)
image_examples = [
    [r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\images\Bar.png"]
]
# video examples
video_examples = [
    [
        r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker\data\example_videos\bench_example.mp4"
    ]
]


with gr.Blocks() as demo:
    with gr.Row():
        gr.Markdown(
            """
            Bar Path Demo
            """
        )
        with gr.Row():
            device = gr.Dropdown(["cpu", "cuda"], value="cpu", label="Select Device")

    # Segment image
    with gr.Tab(label="Image"):
        with gr.Row().style(equal_height=True):
            with gr.Column():
                # input image
                original_image = gr.State(
                    value=None
                )  # store original image without points, default None
                input_image = gr.Image(type="numpy")
                # point prompt
                with gr.Column():
                    selected_points = gr.State([])  # store points
                    with gr.Row():
                        gr.Markdown(
                            "You can click on the image to select points prompt. Default: foreground_point."
                        )
                        undo_button = gr.Button("Undo point")
                    radio = gr.Radio(["top_left", "bottom_right"], label="point labels")
                # text prompt to generate box prompt

                # run button
                button = gr.Button("Auto!")
            # show the image with mask
            with gr.Tab(label="Image+Mask"):
                output_image = gr.Image(type="numpy")
            # show only mask
            with gr.Tab(label="Mask"):
                output_mask = gr.Image(type="numpy")

        def process_example(img, ori_img, sel_p):
            return ori_img, []

        example = gr.Examples(
            examples=image_examples,
            inputs=[input_image, original_image, selected_points],
            outputs=[original_image, selected_points],
            fn=process_example,
            run_on_click=True,
        )

    # Segment video
    with gr.Tab(label="Video"):
        with gr.Row().style(equal_height=True):
            with gr.Column():
                input_video = gr.Video()
                with gr.Row():
                    button_video = gr.Button("Auto!")
            output_video = gr.Video(format="mp4")
        gr.Markdown(
            """
        **Note:** processing video will take a long time, please upload a short video.
        """
        )
        gr.Examples(examples=video_examples, inputs=input_video, outputs=output_video)

    # once user upload an image, the original image is stored in `original_image`
    def store_img(img):
        return img, []  # when new image is uploaded, `selected_points` should be empty

    input_image.upload(store_img, [input_image], [original_image, selected_points])

    # user click the image to get points, and show the points on the image
    def get_point(img, sel_pix, point_type, evt: gr.SelectData):
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

        if img[..., 0][0, 0] == img[..., 2][0, 0]:  # BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img if isinstance(img, np.ndarray) else np.array(img)

    input_image.select(
        get_point,
        [input_image, selected_points, radio],
        [input_image],
    )

    # undo the selected point
    def undo_points(orig_img, sel_pix):
        if isinstance(
            orig_img, int
        ):  # if orig_img is int, the image if select from examples
            temp = cv2.imread(image_examples[orig_img][0])
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        else:
            temp = orig_img.copy()
        # draw points
        if len(sel_pix) != 0:
            print(len(sel_pix))
            sel_pix.pop()
            for point, label in sel_pix:
                cv2.drawMarker(
                    temp,
                    point,
                    colors[label],
                    markerType=markers[label],
                    markerSize=20,
                    thickness=5,
                )

        if temp[..., 0][0, 0] == temp[..., 2][0, 0]:  # BGR to RGB
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        return temp if isinstance(temp, np.ndarray) else np.array(temp)

    undo_button.click(undo_points, [original_image, selected_points], [input_image])

demo.queue().launch(debug=True, enable_queue=True)
