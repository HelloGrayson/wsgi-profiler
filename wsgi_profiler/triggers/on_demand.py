# -*- coding: utf-8 -*-
from __future__ import absolute_import


class OnDemandTrigger(object):

    def __init__(self, required_header_value=None, reporters=()):
        self.required_header_value = required_header_value
        self.reporters = reporters

    def is_detected(self, request):

        prefix = request.get()

        if prefix is None:
            return False

        if not self.required_header_value:
            return True

        if prefix != self.required_header_value:
            return False

        return True
