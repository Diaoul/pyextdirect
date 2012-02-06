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
from exceptions import FormError
from configuration import merge_configurations
import json


class Router(object):
    """Router able to route Ext.Direct requests to their right functions and provide the result

    :param bases: configuration bases
    :type bases: :class:`~pyextdirect.configuration.Base` or list of :class:`~pyextdirect.configuration.Base`

    """
    def __init__(self, bases):
        if not isinstance(bases, list):
            bases = [bases]
        self.configuration = merge_configurations([b.configuration for b in bases])
        self.instances = create_instances(self.configuration)
        self.debug = False

    def route(self, data):
        """Route an Ext Direct request to the appropriate function(s) and provide the response(s)

        :param json data: Ext Direct request
        :return: appropriate response(s)
        :rtype: json

        """
        requests = json.loads(data)
        if not isinstance(requests, list):
            requests = [requests]
        responses = []
        for request in requests:
            responses.append(self.call(request))
        if len(responses) == 1:
            return json.dumps(responses[0])
        return json.dumps(responses)

    def call(self, request):
        """Call the appropriate function

        :param dict request: request that describes the function to call
        :return: response linked to the request that holds the returned value of the called function
        :rtype: dict

        """
        result = None
        try:
            element = self.configuration[request['action']][request['method']]
            data = request['data'] or []
            if isinstance(element, tuple):
                func = getattr(self.instances[element[0]], element[1])
            else:
                func = element
            if func.exposed_form:
                try:
                    func(*data)
                    result = {'success': True}
                except FormError as e:
                    result = {'success': False}
                    if e.errors:
                        result['errors'] = e.errors
            else:
                result = func(*data)
        except Exception as e:
            if self.debug:
                return {'type': 'exception', 'message': str(e), 'where': '%s.%s' % (request['action'], request['method'])}
        return {'type': 'rpc', 'tid': request['tid'], 'action': request['action'], 'method': request['method'], 'result': result}


def create_instances(configuration):
    """Create instances from a configuration

    :param dict configuration: configuration dict. Such a dict is available in :attr:`~pyextdirect.router.Base.configuration`
    :return: class, instance mapping
    :rtype: dict

    """
    instances = {}
    for methods in configuration.itervalues():
        for element in methods.itervalues():
            if not isinstance(element, tuple):
                continue
            cls, _ = element
            if cls not in instances:
                instances[cls] = cls()
    return instances
