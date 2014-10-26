# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random


class ProbabilityTrigger(object):

    def __init__(self, probability=.01, reporters=()):
        self.probability = probability
        self.reporters = reporters

    def is_detected(self, request):

        should_profile = random.random() <= self.probability

        #import ipdb; ipdb.set_trace()

        return should_profile

