# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect


def report(reporter, envelope, request):

    # see what additional args are defined outside contract
    reporter_params = inspect.getargspec(reporter.report)[0]
    reporter_params.remove('self')
    reporter_params.remove('envelope')

    prefix = reporter.__class__.__name__.replace('Reporter', '-')

    # create arg bag for reporter call
    arg_bag = {'envelope': envelope}
    for param in reporter_params:

        argument = request.get(prefix + param)

        if argument:
            arg_bag[param] = argument

    # pass envelope and header params to reporter
    message = reporter.report(**arg_bag)

    if not hasattr(reporter, 'notifiers') or not reporter.notifiers:
        return

    for notifier in reporter.notifiers:
        notify(notifier, message, request)


def notify(notifier, message, request):

    # see what additional args are defined outside contract
    notifier_params = inspect.getargspec(reporter.report)[0]
    notifier_params.remove('self')
    notifier_params.remove('message')

    # create arg bag for notifier call
    arg_bag = {'message': message}

