# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys, time, os.path
from threading import Thread
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
from wsgi_profiler.send import report
from wsgi_profiler.reporters import StdoutReporter
from wsgi_profiler.triggers import AlwaysTrigger


class ProfilerMiddleware(object):

    def __init__(self, app, triggers=(), report_in_background=True):

        if not available:
            raise RuntimeError('the profiler is not available because '
                               'profile or pstat is not installed.')

        self.app = app

        if triggers:
            self.triggers = triggers
        else:
            self.triggers = [
                AlwaysTrigger(reporters=[StdoutReporter(restrictions=[30])])
            ]

        self.report_in_background = report_in_background

    def __call__(self, environ, start_response):

        request = Request(environ)

        # if a profile is triggered
        if not self._is_triggered(request):
            return self.app(environ, start_response)

        # then capture the profile in an envelope
        envelope, body = self._capture(environ, start_response)

        # and report the envelope
        self._report(envelope, request)

        return [body]

    def _is_triggered(self, request):

        for trigger in self.triggers:
            if trigger.is_detected(request):
                return True

        return False

    def _capture(self, environ, start_response):

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

    def _report(self, envelope, request):

        for trigger in self.triggers:

            if not trigger.is_detected(request):
                continue

            for reporter in trigger.reporters:

                # run reporter syncronously if background reporting
                # is turned off or reporter doesnt support async
                if not self.report_in_background or (
                    hasattr(reporter, "ASYNC") and reporter.ASYNC is False
                ):
                    report(reporter, envelope, request)

                # else run the reporter in the background so
                # that the response can be returned to the user quickly
                else:
                    thread = Thread(
                        target=report,
                        args=(reporter, envelope, request)
                    )
                    thread.start()


