from flask import Blueprint, render_template, flash

import random
import time

import plotly
import plotly.graph_objs as go

from detector.detector import Path, path_passes_through_cube

result = Blueprint("result", __name__)

@result.route("/result")
def example_result():
    """
    idea: cache plotly html files, offer "replot" on result page
    idea: when path start/end are quantized, cache volume check results
    """

    start_time = time.perf_counter()
    #p = Path(0.55, 0.55, 1, 0.55, 0.55, 0)
    #print(path_passes_through_cube(p, 0.6, 0.6, 0.6, 0.1, 0.1, 0.1))

    lines = []
    #xs = []
    #ys = []
    #zs = []
    total = 0
    while total < 4000:
        xi, yi, zi = random.random(), random.random(), 1
        xf, yf, zf = xi+(random.random()-0.5), yi+(random.random()-0.5), 0
        if (0 < xf < 1) and (0 < yf < 1):
            p = Path(xi, yi, zi, xf, yf, zf)
            if path_passes_through_cube(p, 0.40, 0.40, 0.04, 0.2, 0.2, 0.2) and random.random() > 0.2:
                continue
            lines.append(([xi, xf], [yi, yf], [zi, zf]))
            #xs += [xi, xf, None]
            #ys += [yi, yf, None]
            #zs += [zi, zf, None]
            total += 1
            #lines.append(None)

    datas = []
    col = '#1f77b4'
    xs = []
    ys = []
    zs = []
    paths_shown = 0
    for line in lines:
        if random.random() > (200/len(lines)):
            continue
        xs += line[0] + [None,]
        ys += line[1] + [None,]
        zs += line[2] + [None,]
        paths_shown += 1
    datas.append(
        go.Scatter3d(x=xs, y=ys, z=zs,
                        hoverinfo="none", connectgaps=False,
                        marker=dict(
                            size=4,
                            color=zs,
                            colorscale='Viridis',
                        ),
                        line=dict(
                            color=col,
                            width=1
                        )
                     )
    )



    """for line in lines:
        if random.random() > (200/len(lines)):
            continue
        col = '#1f77b4'
        p = Path(line[0][0], line[1][0], line[2][0], line[0][1], line[1][1], line[2][1])
        if path_passes_through_cube(p, 0.5, 0.5, 0.5, 0.1, 0.1, 0.1):
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
        ))"""

    x = [(0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4), (0.4, 0.4), (0.6, 0.6), (0.4, 0.4), (0.6, 0.6)]
    y = [(0.4, 0.4), (0.4, 0.4), (0.4, 0.4), (0.4, 0.4), (0.6, 0.6), (0.6, 0.6), (0.6, 0.6), (0.6, 0.6), (0.4, 0.6), (0.4, 0.6), (0.4, 0.6), (0.4, 0.6)]
    z = [(0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4), (0.4, 0.4), (0.6, 0.6), (0.6, 0.6)]

    for i in range(0, len(x)):
        datas.append(go.Scatter3d(
            x=x[i], y=y[i], z=z[i],
            marker=dict(
                size=2,
                color="#0000ff",
            ),
            line=dict(
                color="#0000ff",
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
    max_intersects = 0
    resolution = 15
    total_intersections = 0
    all_intersection_values = []
    for _x in range(0, resolution):
        xs = []
        for _y in range(0, resolution):
            x = _x/resolution
            y = _y/resolution
            intersecting_events = 0
            for line in lines:
                p = Path(line[0][0], line[1][0], line[2][0], line[0][1], line[1][1], line[2][1])
                if path_passes_through_cube(p, x, y, 0.5, 1/resolution, 1/resolution, 0.1):
                    intersecting_events += 1

            #xs.append(x)
            #ys.append(y)
            #zs.append(intersecting_events)
            #if (resolution*0.2 < _x < resolution*0.8) and (resolution*0.2 < _y < resolution*0.8):
            all_intersection_values.append(intersecting_events)
            total_intersections += intersecting_events
            xs.append(intersecting_events)
            max_intersects = max(max_intersects, intersecting_events)
        datas.append(xs)

    print("Total intersecting events: {}".format(total_intersections))

    #for i in range(0, len(datas)):
    #    for j in range(0, len(datas[i])):
    #        datas[i][j] /= max_intersects

    #data = np.array((xs, ys, zs))
    data = [
        go.Surface(
            z=datas,
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
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    html2 = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)

    trace = go.Scatter(
        x = list(range(0, len(all_intersection_values))),
        y = list(sorted(all_intersection_values))
    )
    layout = go.Layout(
        title='Intersection distribution',
        autosize=False,
        width=700,
        height=700,
    )
    fig = go.Figure(data=[trace,], layout=layout)
    html3 = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)


    print("Request time: {}".format(time.perf_counter()-start_time))
    return render_template("example_result.html", charthtml=html, chartdensity=html2, total_events=len(lines), paths_shown=paths_shown, intersect_distribution=html3)