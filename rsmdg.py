from flask import Flask
from flask import render_template, jsonify, request

from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from werkzeug.utils import secure_filename

import os
import os.path as op

# Import blueprints
from detector.views import detector as detector_views
from result.views import result as result_views

APP_ROOT = op.dirname(op.abspath(__file__))
RESULTS_FOLDER = op.join(APP_ROOT, "results")

if not op.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

app = Flask(__name__)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY="verysecretkey",
)

Bootstrap(app)
nav = Nav()
nav.init_app(app)
admin = Admin(app, name="rsmdg", template_mode="bootstrap3")

# register blueprints
app.register_blueprint(detector_views)
app.register_blueprint(result_views)


@nav.navigation()
def nav_bar_renderer():
    items = []
    items.append(View("Home", "index"))
    items.append(View("Detector", "detector.detector_status"))
    items.append(View("Result", "result.example_result"))
    navbar = Navbar("rsmdg", *items)
    html = navbar.render()
    html = html.replace("navbar navbar-default", "navbar navbar-inverse navbar-fixed-top")
    navbar.render = lambda: html
    return navbar


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(**{"STATUS":1, "CURRENT_COUNT":211575})

@app.route("/upload_result", methods=["GET", "POST"])
def upload_result():
    for file in request.files.values():
        filename = secure_filename(file.filename)
        file.save(op.join(RESULTS_FOLDER, filename))
    return jsonify(success=True), 200



if __name__ == '__main__':
    app.run()
