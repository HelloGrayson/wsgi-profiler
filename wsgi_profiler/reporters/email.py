# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, time


class EmailReporter(object):

    def __init__(self, from_address, to_address=None, ):
        self.from_address = from_address
        self.to_address = to_address

    def report(self, envelope, email_to=None):

        # if email_to provided, and no default
        # then return early
        if email_to is None and self.to_address is None:
            return

        # use default email_to if non provided
        to_address = email_to or self.to_address

        title = envelope.get_name()

        body = envelope.get_stats() # this should be summary from stdout

        # attachements = (
        #     envelope.get_compressed_stats(),
        #     envelope.get_compressed_stats(kgrind=True)
        # )

