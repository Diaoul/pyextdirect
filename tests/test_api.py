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
import config
import unittest
from pyextdirect.api import create_api_dict


class APITestCase(unittest.TestCase):
    def test_create_api_dict(self):
        result = create_api_dict(config.Base, 'test.cgi', namespace='My.App.Remote')
        expected = {'url': 'test.cgi',
                    'namespace': 'My.App.Remote',
                    'type': 'remoting',
                    'enableUrlEncode': 'data',
                    'actions': {'Person': [{'name': 'load', 'len': 0},
                                           {'name': 'rename_kiss', 'len': 0},
                                           {'name': 'getAll', 'len': 4},
                                           {'name': 'attack', 'len': 1},
                                           {'name': 'cud', 'len': 2},
                                           {'formHandler': True, 'name': 'save', 'len': 1}],
                                'RenamedService': [{'name': 'hug', 'len': 0},
                                                   {'name': 'renamed_laugh', 'len': 0}],
                                'Basic': [{'name': 'say', 'len': 1}]}}
        self.assertTrue(result == expected)


if __name__ == '__main__':
    unittest.main()

