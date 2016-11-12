from flask import Blueprint, render_template, flash, request

import time

detector = Blueprint("detector", __name__)

class TempDetector:
    running = False
    started_running = 0
    status = "OK"

    @staticmethod
    def running_for():
        return time.time()-TempDetector.started_running

    @staticmethod
    def running_for_hms():
        t = time.time()-TempDetector.started_running
        h, m = divmod(t, 3600)
        m, s = divmod(m, 60)
        return (int(h), int(m), s)

@detector.route("/detector", methods=["GET", "POST"])
def detector_status():
    if request.method == "POST":
        if request.form["submit"] == "start":
            TempDetector.running = True
            TempDetector.started_running = time.time()
            flash("Detector started.", "success")
        if request.form["submit"] == "stop":
            TempDetector.running = False
            flash("Detector stopped. Total run time was {0}h {1}m {2:.02f}s.".format(*TempDetector.running_for_hms()), "success")

    return render_template("detector_status.html", status=TempDetector.status, current_seconds=int(TempDetector.running_for()), run_time="{0}h {1}m {2:.02f}s".format(*TempDetector.running_for_hms()), detector_running=TempDetector.running)