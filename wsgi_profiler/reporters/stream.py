# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from pstats import Stats


class StreamReporter(object):

    def __init__(self, stream=None,
                 sort_by=('time', 'calls'), restrictions=()):
        self.stream = stream or sys.stdout
        self.sort_by = sort_by
        self.restrictions = restrictions

    def report(self, profile, elapsed, request_method, path_info):

        stats = Stats(profile, stream=self.stream)

        stats.sort_stats(*self.sort_by)

        self.stream.write('-' * 80)
        self.stream.write('\nPATH: %r\n' % path_info)
        stats.print_stats(*self.restrictions)
        self.stream.write('-' * 80 + '\n\n')
