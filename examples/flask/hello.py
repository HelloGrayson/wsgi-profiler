from __future__ import absolute_import

from flask import Flask
app = Flask(__name__)



from wsgi_profiler import ProfilingMiddleware
from wsgi_profiler.triggers import HeaderSwitchTrigger
from wsgi_profiler.reporters import FileReporter
from wsgi_profiler.reporters import StreamReporter

app.wsgi_app = ProfilingMiddleware(
    app=app.wsgi_app,
    triggers=[
        HeaderSwitchTrigger()
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
