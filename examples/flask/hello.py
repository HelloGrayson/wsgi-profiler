from __future__ import absolute_import

from flask import Flask

from wsgi_profiler import ProfilerMiddleware
from wsgi_profiler.triggers import OnDemandTrigger
from wsgi_profiler.triggers import ProbabilityTrigger
from wsgi_profiler.reporters import StdoutReporter
from wsgi_profiler.reporters import FileReporter
from wsgi_profiler.reporters import EmailReporter

app = Flask(__name__)

app.wsgi_app = ProfilerMiddleware(app.wsgi_app, [
    OnDemandTrigger(reporters=[
        StdoutReporter(restrictions=[30]),
        FileReporter(profile_dir='profiles'),
        EmailReporter(from_address='grayson.koonce@gmail.com')
    ])
])

@app.route("/")
def hello():

    import time
    import random

    time.sleep(random.random())

    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
