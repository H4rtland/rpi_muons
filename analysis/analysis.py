import inspect
import time
import traceback

import plotly
import plotly.graph_objs as go

from result.models import Result, ResultStatus

class Analysis:
    @staticmethod
    def tick(db):
        new_result = Result.query.filter_by(status=ResultStatus.pending).first()
        if not new_result is None:
            print("Parsing new result {}".format(new_result.id))
            new_result.status = ResultStatus.processing.name
            db.session.commit()
            try:
                Analysis.analyse(new_result, **new_result.parameters)
                new_result.status = ResultStatus.complete.name
            except Exception as exc:
                new_result.status = ResultStatus.failed.name
                new_result.exception = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            finally:
                db.session.commit()

    @staticmethod
    def analyse(result, para1=1, para2=2, **kwargs):
        # Cache kwargs parameters
        local = locals().copy()
        argspec = inspect.getfullargspec(Analysis.analyse)
        kwargs = {name:local[name] for name in argspec.args[-len(argspec.defaults):]}
        result.parameters = kwargs

        paths = []
        with open(result.file, "r") as data_file:
            for line in data_file.readlines():
                points = list(map(float, line.replace("\n", "").split("\t")))
                paths.append(([points[0], points[3]], [points[1], points[4]], [points[2], points[5]]))


        datas = []
        col = '#1f77b4'
        xs = []
        ys = []
        zs = []
        paths_shown = 0
        for line in paths:
            #if random.random() > (400/len(lines)):
            #    continue
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
                    backgroundcolor='rgb(230, 230,230)',
                    range=[0, 1],
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=[0, 1],
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=[-0.05, 1.05],
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

        result.save_plot("path_track", html)

