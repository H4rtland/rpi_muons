from datetime import datetime
import enum
import ast
import os
import os.path as op

from sqlalchemy import Column, Integer, String, DateTime, Enum

from paths import db, PLOT_CACHES_FOLDER

class ResultStatus(enum.Enum):
    pending = "PENDING"
    processing = "PROCESSING"
    complete = "COMPLETE"
    failed = "FAILED"

class Result(db.Model):
    id = Column(Integer, primary_key=True)
    status = Column(Enum(ResultStatus), default=ResultStatus.pending.name)
    creation_date = Column(DateTime, default=datetime.now)
    file = Column(String(200))
    exception = Column(String)

    def get_plot(self, plot_name):
        if op.exists(op.join(self.cache_folder, plot_name + ".html")):
            with open(op.join(self.cache_folder, plot_name + ".html"), "r") as cache_file:
                return cache_file.read()
        return None

    def save_plot(self, plot_name, contents):
        if not op.exists(self.cache_folder):
            os.makedirs(self.cache_folder)
        with open(op.join(self.cache_folder, plot_name + ".html")) as cache_file:
            cache_file.write(contents)

    @property
    def cache_folder(self):
        return op.join(PLOT_CACHES_FOLDER, self.id)