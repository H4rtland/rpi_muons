import inspect
import time
import traceback
import logging
import random

import plotly
import plotly.graph_objs as go

from analysis import layouts

from app import app
from result.models import Result, ResultStatus


class Paths:
    def __init__(self, result):
        self.paths = []
        with open(result.file, "r") as data_file:
            for line in data_file.readlines():
                points = list(map(float, line.replace("\n", "").split("\t")))
                self.paths.append(([points[0], points[3]], [points[1], points[4]], [points[2], points[5]]))

    @property
    def vertical_paths(self):
        for path in self.paths:
            if path[0][0] == path[0][1] and path[1][0] == path[1][1]:
                yield path


class Analysis:
    active_analysis = None

    @staticmethod
    def tick(db):
        new_result = Result.query.filter_by(status=ResultStatus.pending).first()
        if not new_result is None:
            app.logger.log(logging.INFO, "Parsing new result {}".format(new_result.id))
            app.logger.log(logging.INFO, "Parameters: {}".format(new_result.parameters))
            new_result.status = ResultStatus.processing.name
            new_result.exception = ""
            db.session.commit()
            try:
                Analysis.active_analysis.analyse(new_result, **new_result.parameters)
                new_result.status = ResultStatus.complete.name
                app.logger.log(logging.INFO, "Finished parsing result {}".format(new_result.id))
            except Exception as exc:
                new_result.status = ResultStatus.failed.name
                new_result.exception = "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                app.logger.log(logging.WARNING,
                               "Parsing result {} failed: {}: {}".format(new_result.id, exc.__class__.__name__, exc))
            finally:
                db.session.commit()

class LightPulseAnalysis(Analysis):
    @staticmethod
    def analyse(result, histogram_nbins=25, **kwargs):
        # Cache kwargs parameters
        local = locals().copy()
        argspec = inspect.getfullargspec(LightPulseAnalysis.analyse)
        kwargs = {name:local[name] for name in argspec.args[-len(argspec.defaults):]}
        result.parameters = kwargs

        assert histogram_nbins > 0, "must have at least 1 histogram bin"

        with open(result.file, "r") as data_file:
            times = [float(t.strip()) for t in data_file.readlines()]
        
        data = [
            go.Histogram(
                x=times,
                xbins = dict(
                    start=0,
                    end=max(times)+1,
                    size=(max(times)/histogram_nbins),
                ),
                autobinx=False,
            )
        ]

        print(times)
        print("end", max(times))
        print("size", max(times)/histogram_nbins)

        layout = go.Layout(
            title="Pulses histogram",
            xaxis=dict(
                range=[0, max(times)+1],
                title="Time /s",
            ),
            yaxis=dict(
                title="Pulses",
            ),
        )

        fig = go.Figure(data=data, layout=layout)

        html = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="histogram", validate=False)

        result.save_plot("pulses_histogram", html)
        
        

class MuonTrackAnalysis(Analysis):
    @staticmethod
    def analyse(result, shown_muon_paths=500, **kwargs):
        # Cache kwargs parameters
        local = locals().copy()
        argspec = inspect.getfullargspec(MuonTrackAnalysis.analyse)
        kwargs = {name:local[name] for name in argspec.args[-len(argspec.defaults):]}
        result.parameters = kwargs

        assert shown_muon_paths >= 0, "shown_muon_paths can't be negative"

        paths = Paths(result)

        datas = []
        col = '#1f77b4'
        xs = []
        ys = []
        zs = []
        paths_shown = 0
        if shown_muon_paths < len(paths.paths):
            to_show = random.sample(paths.paths, shown_muon_paths)
        else:
            to_show = paths.paths
        for line in paths.paths:
            if not line in to_show:
                continue
            xs += line[0] + [None,]
            ys += line[1] + [None,]
            zs += line[2] + [None,]
            paths_shown += 1

        datas.append(
            go.Scatter3d(x=xs,
                         y=ys,
                         z=zs,
                         hoverinfo="none",
                         connectgaps=False,
                         marker=dict(
                             size=4,
                             color=zs,
                             colorscale='Viridis',
                         ),
                         line=dict(
                             color=col,
                             width=1
                         ),
            )
        )

        fig = dict(data=datas, layout=layouts.path_track_layout)

        html = plotly.offline.plot(fig, auto_open=False, output_type="div", show_link=False, image_width=500, filename="scatter_plot", validate=False)

        result.save_plot("path_track", html)
