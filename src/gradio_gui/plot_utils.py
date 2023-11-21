import plotly.express as px


def return_plot(stats):
    times = list(stats.keys())
    speeds = []
    accelerations = []

    for t in times:
        speeds.append(stats[t]["speeds"])
        accelerations.append(stats[t]["accelerations"])
    fig = px.line(x=times, y=[speeds, accelerations])
    return fig

    # use this to add reps:

    # fig.add_shape(
    #     type="rect",
    #     x0=r[1]["minx"],
    #     x1=r[1]["maxx"],
    #     y0=r[1]["miny"],
    #     y1=r[1]["maxy"],
    #     fillcolor="green",
    #     opacity=0.2,
    # )
