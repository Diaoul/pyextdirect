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
import inspect
import json


def create_api(bases, url, namespace):
    """Create the JS code for the API using a list of configuration :class:`Bases <pyextdirect.configuration.Base>`"""
    return 'Ext.app.REMOTING_API = %s;' % json.dumps(create_api_dict(bases, url, namespace))


def create_api_dict(bases, url, namespace):
    """Create an API dict

    :param bases: configuration bases
    :type bases: :class:`~pyextdirect.configuration.Base` or list of :class:`~pyextdirect.configuration.Base`
    :param string url: URL where the router can be reached
    :param string namespace: client namespace for this API

    """
    api = {'type': 'remoting', 'url': url, 'namespace': namespace, 'actions': {}}
    if not isinstance(bases, list):
        bases = [bases]
    configurations = [b.configuration for b in bases]
    for configuration in configurations:
        for action, methods in configuration.iteritems():
            if action not in api['actions']:
                api['actions'][action] = []
            for method, element in methods.iteritems():
                if isinstance(element, tuple):
                    attrs = len(inspect.getargspec(getattr(element[0], element[1]))[0]) - 1
                else:
                    attrs = len(inspect.getargspec(element)[0])
                api['actions'][action].append({'name': method, 'len': attrs})
    return api
