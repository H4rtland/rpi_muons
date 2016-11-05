from flask import Blueprint, render_template, flash

import random

import plotly
import plotly.graph_objs as go
import numpy as np

from collections import OrderedDict

from detector.detector import Path, path_passes_through_cube

result = Blueprint("result", __name__)

@result.route("/result")
def example_result():

    lines = []
    for _ in range(0, 200):
        xi, yi, zi, xf, yf, zf = random.random(), random.random(), 1, random.random(), random.random(), 0
        lines.append(((xi, yi), (xf, yf), (zi, zf)))

    datas = []
    for line in lines:
        col = '#1f77b4'
        p = Path(line[0][0], line[1][0], line[2][0], line[0][1], line[1][1], line[2][1])
        if path_passes_through_cube(p, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1):
            col = "#ff0000"
        datas.append(go.Scatter3d(
            x=line[0], y=line[1], z=line[2],
            marker=dict(
                size=4,
                color=line[2],
                colorscale='Viridis',
            ),
            line=dict(
                color=col,
                width=1
            ),
            hoverinfo="none",
        ))

    layout = dict(
        width=700,
        height=700,
        autosize=False,
        title='muon paths',
        showlegend = False,
        scene=dict(
            xaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            yaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            zaxis=dict(
                gridcolor='rgb(255, 255, 255)',
                zerolinecolor='rgb(255, 255, 255)',
                showbackground=True,
                backgroundcolor='rgb(230, 230,230)'
            ),
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=-1.7428,
                    y=1.0707,
                    z=0.7100,
                )
            ),
            aspectratio = dict( x=1, y=1, z=0.7 ),
            aspectmode = 'manual',
        ),
    )

    fig = dict(data=datas, layout=layout)

    html = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)





    #xs = []
    #ys = []
    #zs = []
    datas = []

    for _x in range(0, 10):
        xs = []
        for _y in range(0, 10):
            x = _x/10
            y = _y/10
            intersecting_events = 0
            for line in lines:
                p = Path(line[0][0], line[1][0], line[2][0], line[0][1], line[1][1], line[2][1])
                if path_passes_through_cube(p, x, y, 0.5, 0.1, 0.1, 0.1):
                    intersecting_events += 1
            #xs.append(x)
            #ys.append(y)
            #zs.append(intersecting_events)
            xs.append(intersecting_events)
        datas.append(xs)


    #data = np.array((xs, ys, zs))
    data = [
        go.Surface(
            z=datas
        )
    ]
    layout = go.Layout(
        title='Path density at z=0.5',
        autosize=False,
        width=700,
        height=700,
        margin=dict(
            l=65,
            r=50,
            b=65,
            t=90
        )
    )
    fig = go.Figure(data=data, layout=layout)
    html2 = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)



    return render_template("example_result.html", charthtml=html, chartdensity=html2, total_events=len(lines))