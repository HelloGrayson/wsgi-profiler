# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys, time, os.path
try:
    try:
        from cProfile import Profile
    except ImportError:
        from profile import Profile
    from pstats import Stats
    available = True
except ImportError:
    available = False


class ProfilingMiddleware(object):

    def __init__(self, app, triggers=(), reporters=()):

        if not available:
            raise RuntimeError('the profiler is not available because '
                               'profile or pstat is not installed.')

        self.app = app
        self.triggers = triggers
        self.reporters = reporters

    def is_triggered(self, environ):

        for trigger in self.triggers:
            if trigger.is_detected(environ):
                return True

        return False

    def __call__(self, environ, start_response):

        if not self.is_triggered(environ):
            return self.app(environ, start_response)

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

        for reporter in self.reporters:
            reporter.report(
                profile=profile,
                elapsed=elapsed,
                request_method=environ['REQUEST_METHOD'],
                path_info=environ['PATH_INFO']
            )

        return [body]
