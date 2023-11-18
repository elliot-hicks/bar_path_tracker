import cv2
import numpy as np
import gradio as gr

# points color and marker
colors = [(255, 0, 0), (0, 255, 0)]
markers = [1, 5]


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
