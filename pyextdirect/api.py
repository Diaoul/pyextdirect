# -*- coding: utf-8 -*-
# Copyright 2012 Antoine Bertin <diaoulael@gmail.com>
#
# This file is part of pyextdirect.
#
# pyextdirect is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyextdirect is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pyextdirect.  If not, see <http://www.gnu.org/licenses/>.
from collections import defaultdict
from configuration import merge_configurations, SUBMIT
import inspect
import json


def create_api(bases, url, **kwargs):
    """Create the JS code for the API using one or more :class:`Bases <pyextdirect.configuration.Base>`

    :param bases: configuration bases
    :type bases: :class:`~pyextdirect.configuration.Base` or list of :class:`~pyextdirect.configuration.Base`
    :param string url: see :func:`create_api_dict`
    :param \*\*kwargs: see :func:`create_api_dict`

    """
    return 'Ext.app.REMOTING_API = %s;' % json.dumps(create_api_dict(bases, url, **kwargs))


def create_api_dict(bases, url, **kwargs):
    """Create an API dict

    :param bases: configuration bases
    :type bases: :class:`~pyextdirect.configuration.Base` or list of :class:`~pyextdirect.configuration.Base`
    :param string url: URL where the router can be reached
    :param \*\*kwargs: extra keyword arguments to populate the API dict. Most common keyword arguments are *id*, *maxRetries*, *namespace*, *priority* and *timeout*

    .. note::
        Keyword arguments *type*, *url*, *actions* and *enableUrlEncode* will be overridden

    """
    api = kwargs or {}
    api.update({'type': 'remoting', 'url': url, 'actions': defaultdict(list), 'enableUrlEncode': 'data'})
    if not isinstance(bases, list):
        bases = [bases]
    configuration = merge_configurations([b.configuration for b in bases])
    for action, methods in configuration.iteritems():
        for method, element in methods.iteritems():
            if isinstance(element, tuple):
                func = getattr(element[0], element[1])
                attrs = len(inspect.getargspec(func)[0]) - 1
            else:
                func = element
                attrs = len(inspect.getargspec(func)[0])
            spec = {'name': method, 'len': attrs}
            if func.exposed_kind == SUBMIT:
                spec['formHandler'] = True
            api['actions'][action].append(spec)
    return api
