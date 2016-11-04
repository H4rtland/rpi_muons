from flask import Blueprint, render_template, flash

import random

import plotly
import plotly.graph_objs as go

result = Blueprint("result", __name__)

@result.route("/result")
def example_result():

    lines = []
    for _ in range(0, 200):
        lines.append(((random.random(), random.random()), (random.random(), random.random()), (1, 0)))

    datas = []
    for line in lines:
        datas.append(go.Scatter3d(
            x=line[0], y=line[1], z=line[2],
            marker=dict(
                size=4,
                color=line[2],
                colorscale='Viridis',
            ),
            line=dict(
                color='#1f77b4',
                width=1
            ),
            hoverinfo="none",
        ))

    layout = dict(
        width=800,
        height=700,
        autosize=False,
        title='muon paths',
        showlegend = False,
        hovermode=False,
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
            hovermode=False,
        ),
    )

    fig = dict(data=datas, layout=layout)

    html = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)

    return render_template("example_result.html", charthtml=html, total_events=len(lines))