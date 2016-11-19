from datetime import datetime
import enum
import ast
import os
import os.path as op

from sqlalchemy import Column, Integer, String, DateTime, Enum

from app import db, PLOT_CACHES_FOLDER

class ResultStatus(enum.Enum):
    pending = "PENDING"
    processing = "PROCESSING"
    complete = "COMPLETE"
    failed = "FAILED"

class Result(db.Model):
    id = Column(Integer, primary_key=True)
    status = Column(Enum(ResultStatus), default=ResultStatus.pending.name)
    creation_date = Column(DateTime, default=datetime.now)
    file = Column(String)
    exception = Column(String)
    analysis_parameters = Column(String, default="{}")

    def get_plot(self, plot_name):
        if op.exists(op.join(self.cache_folder, plot_name + ".html")):
            with open(op.join(self.cache_folder, plot_name + ".html"), "r") as cache_file:
                return cache_file.read()
        return None

    def save_plot(self, plot_name, contents):
        if not op.exists(self.cache_folder):
            os.makedirs(self.cache_folder)
        with open(op.join(self.cache_folder, plot_name + ".html"), "w") as cache_file:
            cache_file.write(contents)

    def clear_plots(self):
        for filename in os.listdir(self.cache_folder):
            os.unlink(op.join(self.cache_folder, filename))

    @property
    def cache_folder(self):
        return op.join(PLOT_CACHES_FOLDER, str(self.id))

    @property
    def parameters(self):
        return ast.literal_eval(self.analysis_parameters)

    @parameters.setter
    def parameters(self, p):
        self.analysis_parameters = str(p)

    @property
    def filename(self):
        return op.basename(self.file)

    @property
    def failed(self):
        return self.status == ResultStatus.failed

    @property
    def complete(self):
        return self.status == ResultStatus.complete