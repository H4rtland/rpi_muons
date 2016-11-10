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
    todo: move analysis code out of view
    """

    start_time = time.perf_counter()
    #p = Path(0.55, 0.55, 1, 0.55, 0.55, 0)
    #print(path_passes_through_cube(p, 0.6, 0.6, 0.6, 0.1, 0.1, 0.1))

    lines = []
    #xs = []
    #ys = []
    #zs = []
    st = time.time()
    # 10000 Request time: 69.24448532398439 with obstruction
    # 10000 Request time: 70.08756806654017 without obstruction
    # 10000 Request time: 7.622724069724689 with easy checks
    # 100000 Request time: 729.9082427835476 without caching
    # 100000 Request time: 754.6030013966841 with caching
    # 100000 Request time: 76.17804744634259 with easy checks
    while len(lines) < 100000:
        # xi, yi, zi = random.random(), random.random(), 1
        # xf, yf, zf = xi+(random.random()-0.5), yi+(random.random()-0.5), 0
        xi, yi, zi = 0.02 + 0.04*random.randint(0, 24), 0.02 + 0.04*random.randint(0, 24), 1
        xf, yf, zf = xi+(0.04*random.randint(0, 24)-0.5), yi+(0.04*random.randint(0, 24)-0.5), 0
        if (0 < xf < 1) and (0 < yf < 1):
            #p = Path(xi, yi, zi, xf, yf, zf)
            #if path_passes_through_cube(p, 0.40, 0.40, 0.04, 0.2, 0.2, 0.2) and random.random() > 0.2:
            #    continue
            lines.append(([xi, xf], [yi, yf], [zi, zf]))
            #xs += [xi, xf, None]
            #ys += [yi, yf, None]
            #zs += [zi, zf, None]
            #lines.append(None)

    print("Random generation time: {}".format(time.time()-st))

    datas = []
    col = '#1f77b4'
    xs = []
    ys = []
    zs = []
    paths_shown = 0
    for line in lines:
        if random.random() > (400/len(lines)):
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
    st = time.time()
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
                x_i, x_f = line[0][0], line[0][1]
                y_i, y_f = line[1][0], line[1][1]
                z_i, z_f = line[2][0], line[2][1]
                d = 1/resolution

                # Don't bother with exact collision detection for paths with couldn't possibly intersect box (~10x speed gain)
                if ((x_i < x and x_f < x) or (x_i > x+d and x_f > x+d) or (y_i < y and y_f < y) or (y_i > y+d and y_f > y+d)):
                    continue

                p = Path(x_i, y_i, z_i, x_f, y_f, z_f)
                if path_passes_through_cube(p, x, y, 0.5, d, d, d):
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
    print("Intersection time: {}".format(time.time()-st))

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