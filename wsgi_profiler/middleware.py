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

    def __init__(self, app, reporters=()):

        if not available:
            raise RuntimeError('the profiler is not available because '
                               'profile or pstat is not installed.')

        self._app = app
        self._reporters = reporters

    def __call__(self, environ, start_response):

        if not environ.get('HTTP_X_WSGI_PROFILER'):
            return self._app(environ, start_response)

        response_body = []

        def catching_start_response(status, headers, exc_info=None):
            start_response(status, headers, exc_info)
            return response_body.append

        def runapp():
            appiter = self._app(environ, catching_start_response)
            response_body.extend(appiter)
            if hasattr(appiter, 'close'):
                appiter.close()

        profile = Profile()
        start = time.time()
        profile.runcall(runapp)
        body = b''.join(response_body)
        elapsed = time.time() - start

        for reporter in self._reporters:
            reporter.report(
                profile=profile,
                elapsed=elapsed,
                request_method=environ['REQUEST_METHOD'],
                path_info=environ['PATH_INFO']
            )

        return [body]

