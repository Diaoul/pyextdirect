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
from pyextdirect.configuration import create_configuration, expose
from pyextdirect.exceptions import FormError


Base = create_configuration()


class Person(Base):
    """Test class with all possible uses of expose"""
    default_name = 'Anon'
    attack_mark = '!'

    def __init__(self, name=None):
        self.name = name or self.default_name

    def say_hello(self):
        """Unexposed method"""
        return 'Hello ' + self.name

    @expose
    def attack(self, name):
        """Simple exposed method"""
        return self.name.capitalize() + ' attacks ' + name.capitalize() + self.attack_mark

    @expose(method='rename_kiss')
    def kiss(self):
        """Renamed exposed method"""
        return 'Kiss'

    @expose(action='RenamedService')
    def hug(self):
        """Renamed exposed action"""
        return 'Hug'

    @expose(action='RenamedService', method='renamed_laugh')
    def laugh(self):
        """Renamed exposed action and method"""
        return 'Haha'

    @expose(form=True)
    def save(self, name):
        """Form method"""
        if name == 'Diaoul':
            raise FormError('Name already taken', {'message': 'This name is already taken'})
        return {'comment': 'Nice choice!'}


@expose(base=Base, action='Basic')
def say(something):
    """Module level function"""
    return something
