# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, time


class FileReporter(object):

    def __init__(self, profile_dir):
        self.profile_dir = profile_dir

    def report(self, envelope):

        filename = os.path.join(self.profile_dir,
                '%s.%s.%06dms.%d.prof' % (
            envelope.request_method,
            envelope.request_path.strip('/').replace('/', '.') or 'root',
            envelope.elapsed * 1000.0,
            time.time()
        ))

        envelope.profile.dump_stats(filename)

