# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os, time, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE


class EmailReporter(object):

    def __init__(self, from_address, default_to_address=None,
                restricted_domains=()):

        self.from_address = from_address
        self.default_to_address = default_to_address
        self.restricted_domains = restricted_domains
        self.username = username
        self.password = password

    def report(self, envelope, to=None):

        import ipdb; ipdb.set_trace()

        # if email_to provided, and no default
        # then return early
        if to is None and self.default_to_address is None:
            return

        # use default_to_address if none provided
        to_address = to or self.default_to_address

        # ensure address is valid-ish
        if not "@" in to_address:
            return

        # restrict to provided domains
        if self.restricted_domains:
            domain = to_address.split("@")[1]
            if domain not in self.restricted_domains:
                return

        subject = envelope.get_name()

        #body = envelope.get_stats() # this should be summary from stdout
        body = 'hi'

        # attachements = (
        #     envelope.get_compressed_stats(),
        #     envelope.get_compressed_stats(kgrind=True)
        # )



class SmtpAdapter(object):

    def __init__(server, username=None, password=None):

        self.server = smtplib.SMTP(server)
        self.username = username
        self.password password


    def send(from_address, to_address, subject, body, attachements=()):

        self.server.starttls()

        if self.username and self.password:
            self.server.login(self.username, self.password)


        message = MIMEMultipart()
        message['From'] = from_address
        message['To'] = to_address
        message['Subject'] = subject

        for attachement in attachements:
            message.attach(MIMEText(attachement)

        server.sendmail(from_address, to_address, message.as_string())

        self.server.quit()







