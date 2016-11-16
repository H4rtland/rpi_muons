from flask import render_template, jsonify, request

from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Text, Separator
from flask_bootstrap import Bootstrap
from flask_admin import Admin

import paths
from paths import db, app

from analysis import scheduler

# Import blueprints
from detector.views import detector as detector_views
from result.views import result as result_views

# Import models
from result.models import Result


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY="verysecretkey",
    SQLALCHEMY_DATABASE_URI='sqlite:////tmp/rsmdg.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

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

@app.before_first_request
def before_first_request():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run()
