from flask import Flask

import os
import os.path as op

APP_ROOT = op.dirname(op.abspath(__file__))
RESULTS_FOLDER = op.join(APP_ROOT, "results")
PLOT_CACHES_FOLDER = op.join(RESULTS_FOLDER, "plot_caches")

if not op.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

if not op.exists(PLOT_CACHES_FOLDER):
    os.makedirs(PLOT_CACHES_FOLDER)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)