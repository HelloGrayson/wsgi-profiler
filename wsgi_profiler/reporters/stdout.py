# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from pstats import Stats


class StdoutReporter(object):

    ASYNC = False

    def __init__(self, sort_by=('time', 'calls'), restrictions=()):
        self.sort_by = sort_by
        self.restrictions = restrictions

    def report(self, envelope):

        stream = sys.stdout

        stats = Stats(envelope.profile, stream=stream)
        stats.sort_stats(*self.sort_by)

        stream.write('-' * 80)
        stream.write('\nPATH: %r\n' % envelope.request_path)
        stats.print_stats(*self.restrictions)
        stream.write('-' * 80 + '\n\n')
