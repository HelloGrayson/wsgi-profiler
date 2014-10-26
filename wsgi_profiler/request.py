# -*- coding: utf-8 -*-
from __future__ import absolute_import

HEADER_PREFIX = 'X-WSGI-Profiler'


class Request(object):

    def __init__(self, environ):
        self.environ = environ

    def get(self, name=None):

        param = 'HTTP-' + HEADER_PREFIX

        if name:
            param += '-' + name

        param = param.upper().replace('-', '_')

        return self.environ.get(param)
