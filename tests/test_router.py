#!/usr/bin/env python
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
from pyextdirect.router import Router
import config
import json
import unittest


class RouterTestCase(unittest.TestCase):
    def setUp(self):
        self.router = Router(config.Base)

    def test_action_failure(self):
        result = self.router.call({'tid': 1, 'action': 'NotExisting', 'method': 'attack', 'data': ['Stanley']})
        self.assertTrue(result['result'] is None)

    def test_method_failure(self):
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'NotExisting', 'data': ['Stanley']})
        self.assertTrue(result['result'] is None)

    def test_data_failure(self):
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'attack', 'data': ['Stanley', 'NotExisting']})
        self.assertTrue(result['result'] is None)

    def test_debug(self):
        self.router.debug = True
        result = self.router.call({'tid': 1, 'action': 'NoExisting', 'method': 'attack', 'data': ['Stanley']})
        self.assertTrue(result['type'] == 'exception')

    def test_call(self):
        result = self.router.call({'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']})
        self.assertTrue(result['result'] == 'hi')
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'attack', 'data': ['Bill']})
        self.assertTrue(result['result'] == 'Anon attacks Bill!')
        result = self.router.call({'tid': 1, 'action': 'RenamedService', 'method': 'hug', 'data': None})
        self.assertTrue(result['result'] == 'Hug')

    def test_call_form(self):
        result = self.router.call({'extTID': 1, 'extAction': 'Person', 'extMethod': 'save', 'name': 'John'})
        self.assertTrue(result['result']['success'] == True)

    def test_call_form_failure(self):
        result = self.router.call({'extTID': 1, 'extAction': 'Person', 'extMethod': 'save', 'name': 'Diaoul'})
        self.assertTrue(result['result']['success'] == False)
        self.assertTrue(result['result']['errors']['name'] == 'This name is already taken')
        self.assertTrue(result['result']['foo'] == 'bar')

    def test_route(self):
        result = json.loads(self.router.route(json.dumps({'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']})))
        self.assertTrue(result['result'] == 'hi')

    def test_route_multiple(self):
        results = json.loads(self.router.route(json.dumps([{'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']},
                                                          {'tid': 2, 'action': 'Person', 'method': 'rename_kiss', 'data': None}])))
        self.assertTrue(results[0]['tid'] == 1 and results[0]['result'] == 'hi')
        self.assertTrue(results[1]['tid'] == 2 and results[1]['result'] == 'Kiss')

    def test_call_store_read(self):
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'getAll', 'data': None})
        self.assertTrue(result['result'] == {'records': [{'id': 1, 'name': 'Diaoul'}, {'id': 2, 'name': 'John'}, {'id': 3, 'name': u'Beyonc\xe9'}], 'total': 3})

    def test_route_store_destroy(self):
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'destroy', 'data': [{'records': [1]}]})
        self.assertTrue(result['result']['success'] == True)

    def test_route_store_destroy_failure(self):
        result = self.router.call({'tid': 1, 'action': 'Person', 'method': 'destroy', 'data': [{'records': [1, 2]}]})
        self.assertTrue(result['result']['success'] == False)


if __name__ == '__main__':
    unittest.main()
