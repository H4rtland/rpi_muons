import flask
from flask import render_template, jsonify, request

from flask_bootstrap import Bootstrap
from flask_admin import Admin

import os
import os.path as op

import app
from app import db, app, APP_ROOT, ON_RPI

from analysis import scheduler
import navbar

# Import blueprints
from detector.views import detector as detector_views
from result.views import result as result_views

# Import models
from result.models import Result

# Import raspberry pi detector code
if ON_RPI:
    import detector.rpi


app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY="verysecretkey",
    SQLALCHEMY_DATABASE_URI='sqlite:///muon_results.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

Bootstrap(app)
admin = Admin(app, name="rsmdg", template_mode="bootstrap3")

# register blueprints
app.register_blueprint(detector_views)
app.register_blueprint(result_views)


@app.before_first_request
def before_first_request():
    db.create_all()
    db.session().commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/log")
def log():
    with open(op.join(APP_ROOT, "rpi_muons.log")) as logfile:
        log_text = flask.Markup.escape(logfile.read())
        return render_template("generic.html", title="Log", panel_title="Log file", body="<pre>{}</pre>".format(log_text))



if __name__ == '__main__':
    app.run(threaded=True)
