# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, time


class FileReporter(object):

    def __init__(self, profile_dir):
        self.profile_dir = profile_dir

    def report(self, profile, elapsed, request_method, path_info):

        filename = os.path.join(self.profile_dir,
                '%s.%s.%06dms.%d.prof' % (
            request_method,
            path_info.strip('/').replace('/', '.') or 'root',
            elapsed * 1000.0,
            time.time()
        ))

        profile.dump_stats(filename)

