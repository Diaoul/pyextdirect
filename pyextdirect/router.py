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
from configuration import merge_configurations, BASIC, LOAD, SUBMIT
from exceptions import FormError
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

        :param data: Ext Direct request
        :type data: json or dict or list
        :return: appropriate response(s)
        :rtype: json

        """
        if isinstance(data, (dict, list)):
            requests = data
        else:
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
        :return: response linked to the request that holds the value returned by the called function
        :rtype: dict

        """
        result = None
        try:
            if 'extAction' in request:  # DirectSubmit method
                tid = request['extTID']
                action = request['extAction']
                method = request['extMethod']
            else:
                tid = request['tid']
                action = request['action']
                method = request['method']
            element = self.configuration[action][method]
            if isinstance(element, tuple):  # class level function
                func = getattr(self.instances[element[0]], element[1])
            else:  # module level function
                func = element
            if func.exposed_kind == BASIC:  # basic method
                args = request['data'] or []
                result = func(*args)
            elif func.exposed_kind == LOAD:  # DirectLoad method
                args = request['data'] or []
                result = {'success': True, 'data': func(*args)}
            elif func.exposed_kind == SUBMIT:  # DirectSubmit method
                kwargs = request
                for k in ['extAction', 'extMethod', 'extType', 'extTID', 'extUpload']:
                    if k in kwargs:
                        del kwargs[k]
                try:
                    func(**kwargs)
                    result = {'success': True}
                except FormError as e:
                    result = e.extra
                    result['success'] = False
                    if e.errors:
                        result['errors'] = e.errors
        except Exception as e:
            if self.debug:
                return {'type': 'exception', 'message': str(e), 'where': '%s.%s' % (action, method)}
        return {'type': 'rpc', 'tid': tid, 'action': action, 'method': method, 'result': result}


def create_instances(configuration):
    """Create necessary class instances from a configuration with no argument to the constructor

    :param dict configuration: configuration dict like in :attr:`~pyextdirect.configuration.Base.configuration`
    :return: a class-instance mapping
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
