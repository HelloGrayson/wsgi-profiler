from __future__ import absolute_import

from flask import Flask

from wsgi_profiler import ProfilerMiddleware
from wsgi_profiler.triggers import AlwaysTrigger, OnDemandTrigger, ProbabilityTrigger
from wsgi_profiler.reporters import StdoutReporter, FileReporter, EmailReporter

app = Flask(__name__)

app.wsgi_app = ProfilerMiddleware(app.wsgi_app, [
    OnDemandTrigger(reporters=[
        # StdoutReporter(restrictions=[30]),
        # FileReporter(
        #     profile_dir='profiles'
        #     # notifiers=[
        #     #     LogNotifier(),
        #     #     HipChatNotifier(default_room='developers')
        #     # ]
        # ),
        EmailReporter(from_address='grayson.koonce@gmail.com')
    ])
], report_in_background=False)

@app.route("/")
def hello():

    import time
    import random

    time.sleep(random.random())

    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
