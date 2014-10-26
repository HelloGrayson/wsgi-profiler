# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from pstats import Stats


class Envelope(object):

    def __init__(self, profile, time_elapsed, request_path, request_method):

        self.profile = profile
        self.time_elapsed = time_elapsed
        self.request_path = request_path
        self.request_method = request_method

    def get_stats(self, stream=None,
                  sort_by=('time', 'calls'), restrictions=()):

        stream = stream or sys.stdout

        stats = Stats(self.profile, stream=stream)
        stats.sort_stats(*sort_by)

        return stats

    def get_name(self):

        name = '%s.%s.%06dms' % (
            self.request_method,
            self.request_path.strip('/').replace('/', '.') or 'root',
            (self.time_elapsed * 1000.0)
        )

        return name



