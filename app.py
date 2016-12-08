import os
import os.path as op
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP_ROOT = op.dirname(op.abspath(__file__))
RESULTS_FOLDER = op.join(APP_ROOT, "results")
PLOT_CACHES_FOLDER = op.join(RESULTS_FOLDER, "plot_caches")

if not op.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

if not op.exists(PLOT_CACHES_FOLDER):
    os.makedirs(PLOT_CACHES_FOLDER)

ON_RPI = False
if hasattr(os, "uname"):
    if os.uname()[4][:3] == "arm":
        # probably a pi
        ON_RPI = True


db = SQLAlchemy()

app = Flask(__name__)

handler = logging.FileHandler(op.join(APP_ROOT, "rpi_muons.log"))
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


from analysis.analysis import Analysis, MuonTrackAnalysis, LightPulseAnalysis
Analysis.active_analysis = LightPulseAnalysis

# todo: ideally would have choice of analysis type next to detector stop button and reanalyse button
