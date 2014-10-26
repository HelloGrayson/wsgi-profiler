# -*- coding: utf-8 -*-
from __future__ import absolute_import


class HeaderSwitchTrigger(object):

    def __init__(self, key='X-WSGI-Profiler'):
        self.key = key

    def is_detected(self, environ):

        key = self.key.replace('-', '_')
        key = key.upper()
        key = 'HTTP_%s' % key

        if environ.get(key):
            return True

        return False

