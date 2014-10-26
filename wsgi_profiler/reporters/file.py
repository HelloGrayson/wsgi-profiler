# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, time


class FileReporter(object):

    def __init__(self, profile_dir, notifiers=()):
        self.profile_dir = profile_dir
        self.notifiers = notifiers

    def report(self, envelope):

        filename = '%s.%d.prof' % (envelope.get_name(), time.time())
        path = os.path.join(self.profile_dir, filename)

        envelope.profile.dump_stats(path)

        return path

