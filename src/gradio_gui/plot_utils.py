import plotly.express as px
import numpy as np
import pandas as pd


def add_rep_boxes(fig, dataframe, key):
    top = np.max(dataframe[key])
    bottom = np.min(dataframe[key])

    reps = dataframe["rep"]

    for counter, rep in enumerate(set(reps)):
        if rep == 0:  # should be int, otherwise its not in the set
            continue

        rep_times = list(dataframe["time"][dataframe["rep"] == rep])
        rep_start = np.min(rep_times)
        rep_end = np.max(rep_times) - (np.max(dataframe["time"]) / 100)

        if counter % 2 == 0:
            colour = "green"
        else:
            colour = "gray"

        fig.add_shape(
            type="rect",
            x0=rep_start,
            x1=rep_end,
            y0=bottom,
            y1=top,
            fillcolor=colour,
            opacity=0.2,
        )

    return fig


def return_speed_plot(dataframe):
    fig = px.line(dataframe, x="time", y="speed")
    fig = add_rep_boxes(fig, dataframe, key="speed")

    return fig


def return_bar_plot(dataframe):
    reps = set(list(dataframe["rep"]))

    rep_max_speeds = []
    plot_reps = []

    for rep in reps:
        if rep == 0:
            continue

        rep_max_speed = np.max(dataframe["speed"][dataframe["rep"] == rep])
        plot_reps.append(rep)
        rep_max_speeds.append(rep_max_speed)

    fig = px.bar(x=plot_reps, y=rep_max_speeds)

    return fig


def return_acceleration_plot(dataframe):
    fig = px.line(dataframe, x="time", y="acceleration")
    fig = add_rep_boxes(fig, dataframe, key="acceleration")

    return fig
