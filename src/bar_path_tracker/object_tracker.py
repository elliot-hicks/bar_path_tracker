import numpy as np
import os
import sys
import pandas
import cv2
import scipy
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from typing import Tuple, Union, Any


class ObjectTracker:
    def __init__(self) -> None:

        self.tracker = cv2.TrackerCSRT_create()
        self.tracker_type = "CSRT"

        self.frame_height = 1000
        self.frame_width = 1000

    def get_tracker(self) -> Tuple[None, str]:
        """Return tracker (self) and tracker type

        Returns
        -------
        Tuple[None, str]
            self, tracker type string
        """
        return self.tracker, self.tracker_type

    def get_starting_bbox(
        self, video_path: str, plate_size: float
    ) -> Tuple[list[int], tuple[int, int], float]:
        """Draw a starting bounding box around the weight using OpenCV

        Parameters
        ----------
        video_path : str
            Path to video for analysis
        plate_size : float
            Plate size in metres

        Returns
        -------
        Tuple[list[int], float, float]
            _description_
        """
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(video_path)
        ret, frame = video.read()
        if not ret:
            print("cannot read the video")

        # Resize the video for a more convenient view
        frame = cv2.resize(frame, [self.frame_width // 2, self.frame_height // 2])

        # Select the bounding box in the first frame
        bbox: list[int] = cv2.selectROI(frame, False)
        cv2.destroyAllWindows()
        start_bbox_centre: Tuple[int, int] = (
            int(bbox[0] + bbox[2] / 2),
            int(bbox[1] + bbox[3] / 2),
        )

        meters_per_pixel: float = plate_size / max([bbox[2], bbox[3]])

        return bbox, start_bbox_centre, meters_per_pixel

    def smooth_line(
        self, values: list[Union[float, int]], window_length: int = 10
    ) -> np.ndarray:
        """Smooth a line using a sliding average.

        Parameters
        ----------
        values : list[float]
            Line for smoothing
        window_length : int, optional
            Horizon of sliding window, by default 10

        Returns
        -------
        np.ndarray
            Smoothed line
        """

        smoothed_line = np.empty_like(values)

        for i in range(len(values)):
            smoothed_line[i] = np.mean(
                values[
                    max(0, i - window_length // 2) : min(
                        len(smoothed_line), i + window_length // 2
                    )
                ]
            )

        return smoothed_line

    def track_bar_path(
        self,
        video_path,
        starting_bbox,
        starting_bbox_centre,
        meters_per_pixel,
        verbose=False,
    ) -> Tuple[dict[str, float], str]:
        line_colour = (5, 150, 105)
        bar_path = {}
        previous_centre = starting_bbox_centre

        x_positions = []
        y_positions = []

        # load video:
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(video_path)
        time: float = video.get(cv2.CAP_PROP_FPS) / 1000
        ret, frame = video.read()

        frame_width, frame_height = frame.shape[1], frame.shape[0]

        if not ret:
            print("cannot read the video")

        # Resize the video for a more convenient view
        frame = cv2.resize(frame, [frame_width // 1, frame_height // 1])
        mask = np.zeros_like(frame)

        # Select the bounding box in the first frame
        ret = self.tracker.init(frame, starting_bbox)

        counter = 0

        # Start tracking
        while True:
            counter += 1

            ret, frame = video.read()
            time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if not ret:
                break

            frame = cv2.resize(frame, [frame_width // 1, frame_height // 1])
            timer = cv2.getTickCount()
            ret, bbox = self.tracker.update(frame)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            if ret:

                centre = [int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)]
                mask = cv2.line(mask, previous_centre, centre, line_colour, 2)

                centre_x = centre[0] - starting_bbox_centre[0]
                centre_y = starting_bbox_centre[1] - centre[1]

                x_positions.append(centre[1])
                y_positions.append(centre[0])

                bar_path[round(time, 3)] = {
                    "centre_in_meters": [
                        centre_x * meters_per_pixel["x"],
                        centre_y * meters_per_pixel["y"],
                    ],
                    "centre_in_pixels": [centre_x, centre_y],
                    "bounding-box": list(bbox),
                    "centre_global_in_pixels": centre,
                }

            else:
                cv2.putText(
                    frame,
                    "Tracking failure detected",
                    (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

            previous_centre = centre

        x_positions_smoothed = self.smooth_line(x_positions)
        y_positions_smoothed = self.smooth_line(y_positions)

        output_path = f"src/data/results/{self.tracker_type}.mp4"

        # Initialize video writer to save the results
        output = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"XVID"),
            60.0,
            (frame_width // 1, frame_height // 1),
            True,
        )
        index = 0
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(video_path)
        time = video.get(cv2.CAP_PROP_FPS) / 1000
        ret, frame = video.read()
        # Start tracking

        frame_index = 0
        previous_centre = starting_bbox_centre
        empty_mask = np.zeros_like(frame)

        while True:
            ret, frame = video.read()
            time = video.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if not ret:
                break

            frame = cv2.resize(frame, [frame_width // 1, frame_height // 1])

            mask = empty_mask.copy()
            for i in range(max(index - 41, 0), index):
                mask = cv2.line(
                    mask.copy(),
                    [
                        y_positions_smoothed[max(i - 1, 0)],
                        x_positions_smoothed[max(i - 1, 0)],
                    ],
                    [y_positions_smoothed[i], x_positions_smoothed[i]],
                    line_colour,
                    2,
                )

            full_frame = cv2.add(frame, mask)
            output.write(full_frame)
            previous_centre = [y_positions_smoothed[index], x_positions_smoothed[index]]
            index += 1

        video.release()
        output.release()
        cv2.destroyAllWindows()

        return bar_path, output_path

    def differentiate(
        self,
        quantity: list[Union[float, int]],
        time: list[float],
        smooth_quanity: bool = False,
        smoothing_poly_order: int = 5,
    ) -> np.ndaray:
        """Differentiate a list, optionally smoothing it first with sliding
        average.

        Parameters
        ----------
        quantity : list[Union[float, int]]
            Quantity for differentiating w.r.t. time
        time : list[float]
            Time for derrivation
        smooth_quanity : bool, optional
            Smooth the quantity before differentating, by default False
        smoothing_poly_order : int, optional
            Polynomial complexity for savgol filter, by default 5

        Returns
        -------
        np.ndaray
            The time differential of `quantity`
        """

        if smooth_quanity:
            quantity = savgol_filter(quantity, 31, smoothing_poly_order)

        d_quantity = quantity[1:] - quantity[:-1]
        d_time = time[1:] - time[:-1]

        quantity_time = d_quantity / d_time
        quantity_time = np.append(quantity_time, quantity_time[-1])

        return d_quantity / d_time

    def get_stats(
        self,
        bar_path: dict[float, dict[str, float]],
        weight: float,
        verbose: bool = False,
    ) -> dict[float, dict[str, float]]:
        """Collect kinematics for set into a dictionary indexed by time.

        Parameters
        ----------
        bar_path : dict[float, dict[str, float]]
            Tracked bar path with time index
        weight : float
            Weight used for set
        verbose : bool, optional
            To plot stats or not, by default False

        Returns
        -------
        dict[float, dict[str, float]]
            Stats with format:
            stats[time] = {
                "x_distance": x_distances[i],
                "y_distance": y_distances[i],
                "speeds": speeds[i],
                "accelerations": accelerations[i],
            }
        """
        times = np.array(list(bar_path.keys()))
        centres = np.array([entry["centre_in_meters"] for entry in bar_path.values()])

        x_distances = centres[:, 0]
        y_distances = centres[:, 1]

        distances = (x_distances**2 + y_distances**2) ** 0.5
        speeds = self.differentiate(distances, times, smooth_quanity=True)
        accelerations = self.differentiate(speeds, times[1:], smooth_quanity=True)

        speeds = np.pad(
            speeds,
            (0, len(times) - len(speeds)),
            mode="constant",
            constant_values=speeds[-1],
        )
        accelerations = np.pad(
            accelerations,
            (0, len(times) - len(accelerations)),
            mode="constant",
            constant_values=accelerations[-1],
        )

        stats = {}
        for i, t in enumerate(times):
            stats[t] = {
                "x_distance": x_distances[i],
                "y_distance": y_distances[i],
                "speeds": speeds[i],
                "accelerations": accelerations[i],
            }

        if verbose:
            f, axs = plt.subplots(1, 4, figsize=(17, 3))

            axs[0].plot(times, y_distances, c="b", linewidth=2)
            axs[0].set_title("Vertical range")
            axs[0].set_xlabel("Time")

            axs[1].plot(times, x_distances, c="b", linewidth=2)
            axs[1].set_title("Horizontal range")
            axs[1].set_xlabel("Time")

            axs[2].plot(times, speeds, c="r", linewidth=2)
            axs[2].set_title("Speed (m/s)")
            axs[2].set_xlabel("Time")

            axs[3].plot(times, accelerations * weight, c="g", linewidth=1)
            axs[3].set_title("Force (N)")
            axs[3].set_xlabel("Time")

        return stats

    def get_turning_points(
        self, times, displacements, verbose=False
    ) -> dict[int, float]:
        """Find the turning points of a rep using the vertical displacements. Does:
        1. Normalizes displacements
        2. Smooths with Savgol Filter
        3. Counts peaks and troughs using scipy
        4. Finds heights of each turning point
        5. Finds extreme heights and corresponding times



        Parameters
        ----------
        times : list[float]
            List of times in set
        displacements : list[float]
            List of vertical displacements in set
        verbose : bool, optional
            Plot, by default False

        Returns
        -------
        dict[int, float]
            Dict of time indexes and heights corresponding to turning points
        """

        norm_v_displacements = (displacements - displacements.min()) / (
            displacements.max() - displacements.min()
        )
        v_smoothed = savgol_filter(norm_v_displacements, 51, 5)

        peaks = scipy.signal.find_peaks(v_smoothed, height=0.5)
        troughs = scipy.signal.find_peaks(1 - v_smoothed, height=0.5)

        num_peaks = len(peaks[0])
        num_troughs = len(troughs[0])

        heights = np.array([])
        heights = np.append(heights, -1 * troughs[1]["peak_heights"])
        heights = np.append(heights, peaks[1]["peak_heights"])

        turning_point_times = np.array([])
        turning_point_times = np.append(turning_point_times, troughs[0])
        turning_point_times = np.append(turning_point_times, peaks[0])

        x = sorted(zip(turning_point_times, heights))

        turning_points = {0: x[0][1]}

        prev_sign = not x[0][1] < 0

        for i, (t, h) in enumerate(x):
            sign = h < 0
            if sign != prev_sign or i == 0:
                turning_points[int(t)] = h
                prev_h = h
            else:
                if sign:
                    prev_h = min(h, prev_h)
                else:
                    prev_h = max(h, prev_h)

            prev_sign = sign

        extreme_times = list(turning_points.keys())
        extreme_heights = list(turning_points.values())

        num_reps = int(len(turning_points) / 2)

        if verbose:
            plt.scatter(times, displacements)
            plt.scatter(times[extreme_times], displacements[extreme_times])
            print(f"{num_reps} reps detected.")

        return turning_points

    def get_reps(
        self, turning_point_times: list[int], times: dict[int, float]
    ) -> dict[int, dict[str, list[Union[float, int]]]]:
        """Assign rep numbers to times in a set

        Parameters
        ----------
        turning_point_times : list[int]
            Time indices fot turning points
        times : dict[int,float]
            Time values for set

        Returns
        -------
        dict[int, dict[str, list[Union[float, int]]]]
            A dict showing the rep number for every frame index and time value
        """
        reps = {}

        for i in range(len(turning_point_times)):
            if i % 2 != 0 and i + 2 < len(turning_point_times):
                reps[int(i / 2) + 1] = {
                    "frame_inds": [turning_point_times[i], turning_point_times[i + 2]],
                    "times": [
                        times[turning_point_times[i]],
                        times[turning_point_times[i + 2]],
                    ],
                }

        last_rep = max(list(reps.keys()))
        reps[last_rep]["times"][1] = times[-1]

        return reps

    def plot_reps(
        self,
        x_displacements: np.ndarray,
        y_displacements: np.ndarray,
        turning_points: dict[int, float],
        speeds: np.ndarray,
    ) -> None:
        """Plot the reps

        Parameters
        ----------
        x_displacements : np.ndarray
            horizontal distance
        y_displacements : np.ndarray
            vertical distance
        turning_points : dict[int, float]
            Turning points dictt[time index, time value]
        speeds : np.ndarray
            speed
        """
        f, axs = plt.subplots(1, len(turning_points) - 1, figsize=(12, 4))
        extreme_times = list(turning_points.keys())

        for i in range(len(turning_points) - 1):
            if np.mean(speeds[extreme_times[i] : extreme_times[i + 1]]) < 0:
                c = "green"
                title = "Eccentric"
            else:
                c = "red"
                title = "Concentric"

            axs[i].set_xticks([])
            axs[i].set_yticks([])
            axs[i].plot(
                x_displacements[extreme_times[i] : extreme_times[i + 1]],
                y_displacements[extreme_times[i] : extreme_times[i + 1]],
                c=c,
            )
            axs[i].set_title(title)

    def get_set_summary(
        self, bar_path: dict[float, dict[str, float]], weight: float
    ) -> Tuple[dict[float, dict[str, float]], dict[int, dict[str, list[float | int]]]]:
        """Get all stats from tracker

        Parameters
        ----------
        bar_path : dict[float, dict[str, float]]
            Bar path tracking using time: {measurement; value}
        weight : float
            Weight for force calculation

        Returns
        -------
        Tuple[dict[float, dict[str, float]], dict[int, dict[str, list[float | int]]]]
            Stats from `get_stats` and reps from `get_reps`
        """
        stats: dict[float, dict[str, float]] = self.get_stats(bar_path, weight, True)
        times = np.array(list(stats.keys()))

        y_displacements = np.array([entry["y_distance"] for entry in stats.values()])

        turning_points = self.get_turning_points(times, y_displacements, False)
        turning_point_times = np.array(list(turning_points.keys()))
        reps = self.get_reps(turning_point_times, times)

        return stats, reps
