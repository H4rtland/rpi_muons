from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for

import time, random

detector = Blueprint("detector", __name__)

class TempDetector:
    running = False
    started_running = time.time()
    status = "OK"
    last_check_time = 0
    total_muons = 0

    @staticmethod
    def start():
        TempDetector.started_running = time.time()
        TempDetector.total_muons = 0
        TempDetector.last_check_time = 0
        TempDetector.running = True

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
            TempDetector.start()
            flash("Detector started.", "success")
        if request.form["submit"] == "stop":
            TempDetector.running = False
            flash("Detector stopped. Total run time was {0}h {1}m {2:.02f}s.".format(*TempDetector.running_for_hms()), "success")

        # Don't want to repost form on a page refresh
        return redirect(url_for("detector.detector_status"))
    return render_template("detector_status.html", status=TempDetector.status, current_seconds=int(TempDetector.running_for()), run_time="{0}h {1}m {2:.02f}s".format(*TempDetector.running_for_hms()), detector_running=TempDetector.running)

@detector.route("/current_muons")
def current_muons():
    if TempDetector.running:
        for i in range(0, int((TempDetector.running_for()-TempDetector.last_check_time)*100)):
            if random.random() > 0.8:
                TempDetector.total_muons += 1
        TempDetector.last_check_time = TempDetector.running_for()
    else:
        flash("Detector is no longer running.", "error")
    return jsonify(result=TempDetector.total_muons, reload= not TempDetector.running)