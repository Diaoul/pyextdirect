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


__all__ = ['BASIC', 'LOAD', 'SUBMIT', 'STORE_READ', 'ConfigurationMeta', 'create_configuration', 'expose']

#: Basic method
BASIC = 0

#: DirectLoad method
LOAD = 1

#: DirectSubmit method
SUBMIT = 2

#: DirectStore read method
STORE_READ = 3


class ConfigurationMeta(type):
    """Each class created with this metaclass will have its exposed methods registered

    A method can be exposed with the :func:`expose` decorator
    The registration is done by calling :meth:`~Base.register`

    """
    def __init__(cls, name, bases, attrs):
        for attrname, attrvalue in attrs.iteritems():
            if not getattr(attrvalue, 'exposed', False):
                continue
            cls.register((cls, attrname), getattr(attrvalue, 'exposed_action') or name, getattr(attrvalue, 'exposed_method') or attrname)
        return super(ConfigurationMeta, cls).__init__(name, bases, attrs)


def create_configuration(name='Base'):
    """Create a configuration base class

    It is built using :class:`ConfigurationMeta`. Subclassing such a base class
    will register exposed methods

    .. class:: Base

        .. attribute:: configuration

            Configuration dict that can be used by a Router or the API

        .. classmethod:: register(element, action, method)

            Register an element in the :attr:`configuration`

            :param element: the element to register
            :type element: tuple of (class, method name) or function
            :param string action: name of the exposed action that will hold the method
            :param string method: name of the exposed method

    """
    @classmethod
    def register(cls, element, action, method):
        if not action in cls.configuration:
            cls.configuration[action] = {}
        if method in cls.configuration[action]:
            raise ValueError('Method %s already defined for action %s' % (method, action))
        cls.configuration[action][method] = element
    return ConfigurationMeta(name, (object,), {'configuration': {}, 'register': register})


def expose(f=None, base=None, action=None, method=None, kind=BASIC):
    """Decorator to expose a function

    .. note::
        A module function can be decorated but ``base`` parameter has to be specified

    :param f: function to expose
    :type f: function or None
    :param base: base class that can register the function
    :param string action: name of the exposed action that will hold the method
    :param string method: name of the exposed method
    :param kind: kind of the method
    :type kind: :data:`BASIC` or :data:`LOAD` or :data:`SUBMIT`

    """
    def expose_f(f):
        f.exposed = True
        f.exposed_action = action
        f.exposed_method = method
        f.exposed_kind = kind
        return f

    def register_f(f):
        f = expose_f(f)
        base.register(f, action or f.__module__, method or f.__name__)
        return f

    if f is not None:  # @expose case (no parameters)
        return expose_f(f)
    if base is not None:  # module-level function case
        return register_f
    return expose_f


def merge_configurations(configurations):
    """Merge configurations together and raise error if a conflict is detected

    :param configurations: configurations to merge together
    :type configurations: list of :attr:`~pyextdirect.configuration.Base.configuration` dicts
    :return: merged configurations as a single one
    :rtype: dict

    """
    configuration = {}
    for c in configurations:
        for k, v in c.iteritems():
            if k in configuration:
                raise ValueError('%s already in a previous base configuration' % k)
            configuration[k] = v
    return configuration
