import os
import os.path as op

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP_ROOT = op.dirname(op.abspath(__file__))
RESULTS_FOLDER = op.join(APP_ROOT, "results")
PLOT_CACHES_FOLDER = op.join(RESULTS_FOLDER, "plot_caches")

if not op.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

if not op.exists(PLOT_CACHES_FOLDER):
    os.makedirs(PLOT_CACHES_FOLDER)


db = SQLAlchemy()

app = Flask(__name__)