# -*- coding: utf-8 -*-
from __future__ import absolute_import


class OnDemandTrigger(object):

    def __init__(self, header_key='Enabled',
                header_value=None, reporters=()):

        self.header_key = header_key
        self.header_value = header_value
        self.reporters = reporters

    def is_detected(self, request):

        header = request.get(self.header_key)

        if header is None:
            return False

        if not self.header_value:
            return True

        if header != self.header_value:
            return False

        return True
