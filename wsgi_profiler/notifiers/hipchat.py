# -*- coding: utf-8 -*-
from __future__ import absolute_import


class HipchatNotifier(object):

    def __init__(self, default_room):
        self.default_room = default_room

    def notify(message, room=False):
