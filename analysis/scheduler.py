from apscheduler.schedulers.background import BackgroundScheduler

from app import app, db

from analysis.analysis import Analysis

scheduler = BackgroundScheduler()

def run_analysis():
    with app.app_context():
        Analysis.tick(db)
        db.session.commit()

ding = scheduler.add_job(run_analysis, "interval", seconds=10)
scheduler.start()