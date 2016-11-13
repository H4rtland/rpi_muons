import os
import os.path as op

APP_ROOT = op.dirname(op.abspath(__file__))
RESULTS_FOLDER = op.join(APP_ROOT, "results")

if not op.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)