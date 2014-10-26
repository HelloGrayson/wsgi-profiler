# -*- coding: utf-8 -*-
from __future__ import absolute_import


class AlwaysTrigger(object):

    def __init__(self, reporters=()):
        self.reporters = reporters

    def is_detected(self, request):

        return True
