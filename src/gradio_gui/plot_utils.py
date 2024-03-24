import plotly.express as px
import numpy as np
from pandas import DataFrame
from plotly.graph_objects import Figure


def add_rep_boxes(fig: Figure, dataframe: DataFrame, key: str) -> Figure:
    """Annotate plot with rep regions (add a coloured patch in
    alternating colours to distinguish reps.)

    Parameters
    ----------
    fig : Figure
        Plotly figure for rep boxes to be added
    dataframe : DataFrame
        bar path data
    key : str
        metric for plot to determine box min and max height.

    Returns
    -------
    Figure
        Updated plot with added rep boxes annotated
    """
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
            colour = "white"
        else:
            colour = "gray"

        fig.add_shape(
            type="rect",
            x0=rep_start,
            x1=rep_end,
            y0=bottom,
            y1=top,
            fillcolor=colour,
            opacity=0.1,
        )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def return_speed_plot(dataframe: DataFrame) -> Figure:
    """Plot speed from bar path data

    Parameters
    ----------
    dataframe : DataFrame
        Bar path data

    Returns
    -------
    Figure
        plotly line plot of speed against times
    """
    fig = px.line(
        dataframe,
        x="time",
        y="speed",
        labels={"time": "Time (s)", "speed": "Vertical Speed (M/s)"},
    )
    fig = add_rep_boxes(fig, dataframe, key="speed")
    fig["data"][0]["line"]["color"] = "#047857"
    fig.update_layout(
        {
            "paper_bgcolor": "rgb(30, 30, 30)",
            "plot_bgcolor": "rgb(30, 30, 30)",
            "font_color": "#047857",
            "font_size": 20,
        }
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig["data"][0]["line"]["width"] = 3
    return fig


def return_distance_plot(dataframe: DataFrame) -> Figure:
    """Plot distance from bar path data

    Parameters
    ----------
    dataframe : DataFrame
        Bar path data

    Returns
    -------
    Figure
        Plotly line plot of distance against times
    """
    fig = px.line(
        dataframe,
        x="time",
        y="y_distance",
        labels={
            "y_distance": "Height (M)",
            "time": "Time(s)",
        },
    )
    fig = add_rep_boxes(fig, dataframe, key="y_distance")
    fig["data"][0]["line"]["color"] = "#047857"
    fig.update_layout(
        {
            "paper_bgcolor": "rgb(30, 30, 30)",
            "plot_bgcolor": "rgb(30, 30, 30)",
            "font_color": "#047857",
            "font_size": 20,
        }
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig["data"][0]["line"]["width"] = 3

    return fig


def return_max_speed_bar_plot(dataframe: DataFrame) -> Figure:
    """Return bar plot of max speeds for each rep.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe of bar path stats

    Returns
    -------
    Figure
        Bar plot of max speeds against time.
    """
    reps = set(list(dataframe["rep"]))

    rep_max_speeds = []
    plot_reps = []

    for rep in reps:
        if rep == 0:
            continue

        rep_max_speed = np.max(dataframe["speed"][dataframe["rep"] == rep])
        plot_reps.append(rep)
        rep_max_speeds.append(rep_max_speed)

    fig = px.bar(
        x=plot_reps,
        y=rep_max_speeds,
        labels={"x": "Rep", "y": "Maximum Vertical Speed M/s"},
    )
    fig.update_traces(marker_color="#059669")
    fig.update_layout(
        {
            "paper_bgcolor": "rgb(30, 30, 30)",
            "plot_bgcolor": "rgb(30, 30, 30)",
            "font_color": "#047857",
            "font_size": 18,
        }
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def return_max_acceleration_bar_plot(dataframe: DataFrame) -> Figure:
    """Return bar plot of max accelerations for each rep.

    Parameters
    ----------
    dataframe : DataFrame
        Dataframe of bar path stats

    Returns
    -------
    Figure
        Bar plot of max speeds against time.
    """
    reps = set(list(dataframe["rep"]))

    rep_max_accelerations = []
    plot_reps = []

    for rep in reps:
        if rep == 0:
            continue

        rep_max_accel = np.max(dataframe["acceleration"][dataframe["rep"] == rep])
        plot_reps.append(rep)
        rep_max_accelerations.append(rep_max_accel)

    fig = px.bar(
        x=plot_reps,
        y=rep_max_accelerations,
        labels={"x": "Rep", "y": "Maximum Vertical Acceleration M/s^2"},
    )
    fig.update_traces(marker_color="#059669")
    fig.update_layout(
        {
            "paper_bgcolor": "rgb(30, 30, 30)",
            "plot_bgcolor": "rgb(30, 30, 30)",
            "font_color": "#047857",
            "font_size": 18,
        }
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig


def return_acceleration_plot(dataframe: DataFrame) -> Figure:
    """Plot acceleration from bar path data

    Parameters
    ----------
    dataframe : DataFrame
        Bar path data

    Returns
    -------
    Figure
        Plotly line plot of acceleration against times
    """
    fig = px.line(
        dataframe,
        x="time",
        y="acceleration",
        labels={
            "acceleration": "Vertical Acceleration (M/s^2)",
            "time": "Time(s)",
        },
    )
    fig = add_rep_boxes(fig, dataframe, key="acceleration")
    fig["data"][0]["line"]["color"] = "#047857"
    fig["data"][0]["line"]["width"] = 3

    fig.update_layout(
        {
            "paper_bgcolor": "rgb(30, 30, 30)",
            "plot_bgcolor": "rgb(30, 30, 30)",
            "font_color": "#047857",
            "font_size": 20,
        }
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig
