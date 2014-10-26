# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys, time, os.path, inspect
try:
    try:
        from cProfile import Profile
    except ImportError:
        from profile import Profile
    from pstats import Stats
    available = True
except ImportError:
    available = False

from wsgi_profiler.envelope import Envelope
from wsgi_profiler.request import Request


class ProfilerMiddleware(object):

    def __init__(self, app, triggers=()):

        if not available:
            raise RuntimeError('the profiler is not available because '
                               'profile or pstat is not installed.')

        self.app = app
        self.triggers = triggers

    def __call__(self, environ, start_response):

        request = Request(environ)

        # if a profile is triggered
        if not self.is_triggered(request):
            return self.app(environ, start_response)

        # then capture the profile in an envelope
        envelope, body = self.capture(environ, start_response)

        # and report the envelope
        self.report(envelope, request)

        return [body]

    def is_triggered(self, request):

        for trigger in self.triggers:
            if trigger.is_detected(request):
                return True

        return False

    def capture(self, environ, start_response):

        response_body = []

        def catching_start_response(status, headers, exc_info=None):
            start_response(status, headers, exc_info)
            return response_body.append

        def runapp():
            appiter = self.app(environ, catching_start_response)
            response_body.extend(appiter)
            if hasattr(appiter, 'close'):
                appiter.close()

        profile = Profile()
        start = time.time()
        profile.runcall(runapp)
        body = b''.join(response_body)
        elapsed = time.time() - start

        envelope = Envelope(
            profile=profile,
            time_elapsed=elapsed,
            request_path=environ['PATH_INFO'],
            request_method=environ['REQUEST_METHOD']
        )

        return (envelope, body)

    def report(self, envelope, request):

        for trigger in self.triggers:

            if not trigger.is_detected(request):
                continue

            for reporter in trigger.reporters:

                # see what additional args are defined outside contract
                reporter_params = inspect.getargspec(reporter.report)[0]
                reporter_params.remove('self')
                reporter_params.remove('envelope')

                # create arg bag for reporter call
                arg_bag = {'envelope': envelope}
                for param in reporter_params:
                    if request.get(param):
                        arg_bag[param] = request.get(param)

                # pass envelope and header params to reporter
                reporter.report(**arg_bag)
