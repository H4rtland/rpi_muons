from flask import Blueprint, render_template, flash

detector = Blueprint("detector", __name__)

@detector.route("/detector")
def detector_status():
    flash("Everything is fine.", )
    return render_template("detector_status.html", status="OK")