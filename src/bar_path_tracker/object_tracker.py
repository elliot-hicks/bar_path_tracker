import numpy as np
import os
import sys
import pandas
import cv2
import scipy
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


class ObjectTracker:
    def __init__(self) -> None:
        self.repo_path = r"C:\Users\ellio\OneDrive\Desktop\GitHub\bar_path_tracker"
        self.video_path = r"src\data\example_videos\bench_example.mp4"

        self.tracker = cv2.TrackerCSRT_create()
        self.tracker_type = "CSRT"

        self.frame_height = 1000
        self.frame_width = 1000

    def open_and_display_video(self, path: str) -> None:
        """Open Video
        _
        """
        vid = cv2.VideoCapture(os.path.join(self.repo_path, path))
        if vid.isOpened() == False:
            print("Error opening video stream or file")
        else:
            print(f"Playing video at {path}. Hit 'q' to quit.")

        while vid.isOpened():
            # Capture frame-by-frame
            ret, frame = vid.read()

            if ret == True:
                cv2.imshow("Video", frame)
                if cv2.waitKey(25) & 0xFF == ord("q"):
                    break
            else:
                break
        # When everything done, release the video capture object
        vid.release()
        # Closes all the frames
        cv2.destroyAllWindows()

    def get_tracker(self):
        return self.tracker, self.tracker_type

    def get_starting_bbox(self, video_path, plate_size):
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(os.path.join(self.repo_path, video_path))
        ret, frame = video.read()
        if not ret:
            print("cannot read the video")

        # Resize the video for a more convenient view
        frame = cv2.resize(frame, [self.frame_width // 2, self.frame_height // 2])

        # Select the bounding box in the first frame
        bbox = cv2.selectROI(frame, False)
        cv2.destroyAllWindows()
        start_bbox_centre = (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))

        meters_per_pixel = plate_size / max([bbox[2], bbox[3]])

        return bbox, start_bbox_centre, meters_per_pixel

    def smooth_line(self, values: list[float], window_length: int = 20):

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
    ):
        line_colour = (5, 150, 105)

        frame_height = 1000
        frame_width = 1000
        bar_path = {}
        previous_centre = starting_bbox_centre

        x_positions = []
        y_positions = []

        # load video:
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(os.path.join(self.repo_path, video_path))
        time = video.get(cv2.CAP_PROP_FPS) / 1000
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
                top_left = (int(bbox[0]), int(bbox[1]))  # top left
                bottom_right = (
                    int(bbox[0] + bbox[2]),
                    int(bbox[1] + bbox[3]),
                )  # bottom right
                centre = [int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)]
                mask = cv2.line(mask, previous_centre, centre, line_colour, 2)
                # frame = cv2.rectangle(frame, top_left, bottom_right, box_colour, 2, 1)
                # frame = cv2.circle(frame, centre, 5, box_colour)
                centre_x = centre[0] - starting_bbox_centre[0]
                centre_y = starting_bbox_centre[1] - centre[1]

                x_positions.append(centre[1])
                y_positions.append(centre[0])

                bar_path[round(time, 3)] = {
                    "centre_in_meters": [
                        centre_x * meters_per_pixel,
                        centre_y * meters_per_pixel,
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
        video = cv2.VideoCapture(os.path.join(self.repo_path, video_path))
        time = video.get(cv2.CAP_PROP_FPS) / 1000
        ret, frame = video.read()
        # Start tracking

        frame_index = 0
        previous_centre = starting_bbox_centre
        empty_mask = np.zeros_like(frame)

        print(empty_mask.shape)
        print(frame.shape)

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
        self, quantity, time, smooth_quanity=False, smoothing_poly_order=5
    ):
        if smooth_quanity:
            quantity = savgol_filter(quantity, 51, smoothing_poly_order)

        d_quantity = quantity[1:] - quantity[:-1]
        d_time = time[1:] - time[:-1]

        quantity_time = d_quantity / d_time
        quantity_time = np.append(quantity_time, quantity_time[-1])

        return d_quantity / d_time

    def get_stats(self, bar_path, weight, verbose=False):
        times = np.array(list(bar_path.keys()))
        centres = np.array([entry["centre_in_meters"] for entry in bar_path.values()])

        x_distances = centres[:, 0]
        y_distances = centres[:, 1]
        speeds = self.differentiate(y_distances, times, smooth_quanity=True)
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

    def get_turning_points(self, times, displacements, verbose=False):
        norm_v_displacements = (displacements - displacements.min()) / (
            displacements.max() - displacements.min()
        )
        v_smoothed = savgol_filter(norm_v_displacements, 51, 5)

        peaks = scipy.signal.find_peaks(v_smoothed, height=0.5)
        troughs = scipy.signal.find_peaks(1 - v_smoothed, height=0.5)

        num_peaks = len(peaks[0])
        num_troughs = len(troughs[0])
        # num_reps = max(num_peaks, num_troughs)

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

    def get_reps(self, turning_point_times, times):
        reps = {}

        for i in range(len(turning_point_times)):
            if i % 2 == 0 and i + 2 < len(turning_point_times):
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

    def plot_reps(self, x_displacements, y_displacements, turning_points, speeds):
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

    def show_video_with_stats(self, video_path, bar_path, stats, reps):
        line_colour = (255, 255, 255)

        # load video:
        cv2.destroyAllWindows()
        video = cv2.VideoCapture(os.path.join(self.repo_path, video_path))
        time = video.get(cv2.CAP_PROP_FPS) / 1000
        ret, frame = video.read()
        if not ret:
            print("cannot read the video")

        # Resize the video for a more convinient view
        frame = cv2.resize(frame, [self.frame_width // 2, self.frame_height // 2])
        mask = np.zeros_like(frame)

        # Initialize video writer to save the results
        output = cv2.VideoWriter(
            f"data/results/{self.tracker_type}_with_stats.mp4",
            cv2.VideoWriter_fourcc(*"XVID"),
            60.0,
            (self.frame_width // 2, self.frame_height // 2),
            True,
        )

        previous_centre = None

        # Start tracking
        while True:
            ret, frame = video.read()
            time = round(video.get(cv2.CAP_PROP_POS_MSEC) / 1000, 3)

            if not ret:
                break
            rep_number = [
                n
                for (n, v) in reps.items()
                if (time <= v["times"][1] and time >= v["times"][0])
            ][0]

            frame = cv2.resize(frame, [self.frame_width // 2, self.frame_height // 2])
            timer = cv2.getTickCount()
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            if time in list(bar_path.keys()):
                centre = bar_path[round(time, 3)]["centre_global_in_pixels"]
                if previous_centre is not None:
                    mask = cv2.line(mask, previous_centre, centre, line_colour, 2)
                previous_centre = centre
                speed = stats[time]["speeds"]
                acceleration = stats[time]["accelerations"]
                cv2.putText(
                    frame,
                    "Speed: " + str(round(speed, 1)) + "m/s",
                    (0, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    1,
                )
                cv2.putText(
                    frame,
                    "Acceleration: " + str(round(acceleration, 1)) + "m/s^2",
                    (0, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    1,
                )
                cv2.putText(
                    frame,
                    "Rep Number: " + str(int(rep_number)),
                    (0, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    1,
                )
            # Show stats:
            cv2.putText(
                frame,
                self.tracker_type + " Tracker",
                (0, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                1,
            )
            cv2.putText(
                frame,
                "Time: " + str(round(time, 1)) + "s",
                (0, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                1,
            )
            full_frame = cv2.add(frame, mask)
            cv2.imshow("Tracking", full_frame)
            output.write(full_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        video.release()
        output.release()
        cv2.destroyAllWindows()

    def get_set_summary(self, bar_path, weight):
        stats = self.get_stats(bar_path, weight, True)
        times = np.array(list(stats.keys()))

        y_displacements = np.array([entry["y_distance"] for entry in stats.values()])

        turning_points = self.get_turning_points(times, y_displacements, False)
        turning_point_times = np.array(list(turning_points.keys()))
        reps = self.get_reps(turning_point_times, times)

        return stats, reps
