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


class Error(Exception):
    """Base class for pyextdirect exceptions"""
    pass


class FormError(Error):
    """Raised when an error occurs in a form handler method

    A result dict can be provided and will be returned to the client

    :param dict errors: result returned to the client

    For example::

        @expose(form=True)
        def save(self, firstname, lastname):
            errors = {}
            if len(firstname) < 3:
                errors['firstname'] = 'Invalid length'
            if not lastname:
                errors['lastname'] = 'Missing'
            if errors:
                raise FormError(errors)
            # ...

    Will return the dict ``{'success': False, 'message': 'Last name is missing'}`` as result in a response

    """
    def __init__(self, errors):
        self.errors = errors or {}

    def __str__(self):
        return repr(self.errors)
