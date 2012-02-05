.. pyextdirect documentation master file, created by
   sphinx-quickstart on Sat Feb  4 18:27:48 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============
Release v\ |version|

Python implementation of `Ext Direct Server-side Stack <http://www.sencha.com/products/extjs/extdirect>`_

Example
=======
For this simple example we are going to consider that you have knowledge of the client part.

First, in ``config.py``::

    from pyextdirect.configuration import create_configuration, expose
    
    Base = create_configuration()
    
    class Test(Base):
        @expose
        def upper(self, string):
            return string.upper()
    
    @expose(base=Base, action='Test')
    def lower(string):
        return string.lower()

Then, ``api.py``::

    from pyextdirect.api import create_api
    import config
    
    if __name__ == '__main__':
        print "Content-type: text/javascript\r\n\r\n"
        print create_api(config.Base)

And finally ``router.py``::

    from pyextdirect.router import Router
    import config
    import cgi
    
    if __name__ == '__main__':
        router = Router(config.Base)
        fs = cgi.FieldStorage()
        print "Content-type: application/json\r\n\r\n"
        print router.route(fs.value)

API Documentation
=================

Configuration
-------------
.. automodule:: pyextdirect.configuration
    :members:

Router
------
.. automodule:: pyextdirect.router
    :members:

API
---
.. automodule:: pyextdirect.api
    :members:
