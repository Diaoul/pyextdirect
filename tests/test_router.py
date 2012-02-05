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
from pyextdirect.configuration import create_configuration, expose
import unittest
import json


class RouterTestCase(unittest.TestCase):
    def setUp(self):
        Base = create_configuration()
        class Language(Base):
            shout_mark = '!'

            def say_hello(self):
                return 'hello'

            @expose
            def shout(self, name):
                return self.say_hello() + ' ' + name + self.shout_mark

            @expose(method='shorten')
            def cut(self, string, max_len):
                return string[:max_len]
        
        @expose(base=Base, action='Basic')
        def say(something):
            return something
        self.router = Router(Base)
        self.router.debug = False

    def test_action_failure(self):
        result = self.router.call({'tid': 1, 'action': 'NoExisting', 'method': 'say', 'data': ['hi']})
        self.assertTrue(result['result'] is None)

    def test_method_failure(self):
        result = self.router.call({'tid': 1, 'action': 'Language', 'method': 'not_existing', 'data': ['hi']})
        self.assertTrue(result['result'] is None)

    def test_data_failure(self):
        result = self.router.call({'tid': 1, 'action': 'Language', 'method': 'say', 'data': ['hi', 'extra', 'args']})
        self.assertTrue(result['result'] is None)

    def test_debug(self):
        self.router.debug = True
        result = self.router.call({'tid': 1, 'action': 'NoExisting', 'method': 'say', 'data': ['hi']})
        self.assertTrue(result['type'] == 'exception')

    def test_call(self):
        result = self.router.call({'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']})
        self.assertTrue(result['result'] == 'hi')
        result = self.router.call({'tid': 1, 'action': 'Language', 'method': 'shout', 'data': ['Bill']})
        self.assertTrue(result['result'] == 'hello Bill!')
        result = self.router.call({'tid': 1, 'action': 'Language', 'method': 'shorten', 'data': ['shortening test', 13]})
        self.assertTrue(result['result'] == 'shortening te')

    def test_route_simple(self):
        result = json.loads(self.router.route(json.dumps({'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']})))
        self.assertTrue(result['result'] == 'hi')

    def test_route_multiple(self):
        results = json.loads(self.router.route(json.dumps([{'tid': 1, 'action': 'Basic', 'method': 'say', 'data': ['hi']},
                                                          {'tid': 1, 'action': 'Language', 'method': 'shout', 'data': ['Bill']}])))
        self.assertTrue(results[0]['result'] == 'hi')
        self.assertTrue(results[1]['result'] == 'hello Bill!')


if __name__ == '__main__':
    pass
