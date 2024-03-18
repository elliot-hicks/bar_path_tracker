import cv2
import numpy as np
import gradio as gr
from typing import Tuple

# points color and marker
colors = [(5, 150, 105), (5, 150, 105)]
markers = [0, 0]


# once user upload an image, the original image is stored in `original_image`
def store_img(img: np.ndarray):
    return img, []  # when new image is uploaded, `selected_points` should be empty


def get_point(img: np.ndarray, sel_pix: list, evt: gr.SelectData) -> np.ndarray:
    """User click the image to get points, and show the points on the image

    Parameters
    ----------
    img : np.ndarray
        Bbox image
    sel_pix : list
        List of selected coords for bounding box
    evt : gr.SelectData
        Event for selecting pixel (mouse click)

    Returns
    -------
    np.ndarray
        Image frame with selected pixel shown.
    """
    if len(sel_pix) < 2:
        sel_pix.append(evt.index)  # append the background_point

        # draw points
        for point in sel_pix:
            cv2.drawMarker(
                img,
                point,
                colors[0],
                markerType=markers[0],
                markerSize=0,
                thickness=5,
            )

        if len(sel_pix) == 2:
            start_point = sel_pix[0]
            end_point = sel_pix[1]
            color = colors[0]
            thickness = 2
            cv2.rectangle(img, start_point, end_point, color, thickness)
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img if isinstance(img, np.ndarray) else np.array(img)


# undo the selected point
def undo_points(orig_img: np.ndarray, sel_pix: list) -> Tuple[np.ndarray, list[float]]:
    """Undo a selected point

    Parameters
    ----------
    orig_img : np.ndarray
        Original first frame image for the bbox
    sel_pix : list
        Selected pixels

    Returns
    -------
    Tuple[np.ndarray, list[float]]
        New bbox image, new selected points.
    """
    temp = orig_img.copy()

    # draw points
    if len(sel_pix) != 0:
        sel_pix.pop()
        for point in sel_pix:
            cv2.drawMarker(
                temp,
                point,
                colors[0],
                markerType=markers[0],
                markerSize=00,
                thickness=5,
            )

    return np.array(temp), sel_pix


def show_points(selected_points: list):
    return gr.update(value=selected_points)
