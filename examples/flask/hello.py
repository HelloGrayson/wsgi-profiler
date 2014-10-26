from __future__ import absolute_import

from flask import Flask
from wsgi_profiler import ProfilingMiddleware
from wsgi_profiler.triggers import HeaderPresenceTrigger
from wsgi_profiler.reporters import FileReporter
from wsgi_profiler.reporters import StreamReporter

app = Flask(__name__)

app.wsgi_app = ProfilingMiddleware(
    app=app.wsgi_app,
    triggers=[
        HeaderPresenceTrigger()
    ],
    reporters=[
        StreamReporter(restrictions=[30]),
        FileReporter(profile_dir='profiles'),
    ]
)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
