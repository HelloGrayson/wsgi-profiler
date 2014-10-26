# -*- coding: utf-8 -*-
from __future__ import absolute_import


class HeaderPresenceTrigger(object):

    def __init__(self, header='X-WSGI-Profiler'):
        self.header = header

    def is_detected(self, environ):

        header = self.header.replace('-', '_')
        header = header.upper()
        header = 'HTTP_%s' % header

        if environ.get(header):
            return True

        return False

