# -*- coding: utf-8 -*-
from __future__ import absolute_import

_config = {

    'aws_access_key_id': None,
    'aws_secret_access_key': None,
    'aws_region': None,

    'hipchat_token': None,
    'hipchat_room': None
}


def set(conf_dict):
    for key, value in conf_dict.items():
        if key not in _config:
            raise Exception("%s is not a valid config item" % key)
        _config[key] = value


def get(key):
    return _config.get(key)
