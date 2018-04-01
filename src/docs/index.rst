Adata documentation
===================

*Under construction!*

The purpose of this application is to handle events with custom python scripts. The main interface is an interactive python console with programmable commands and plug-in modules. It is based on a publisher/subscriber messaging pattern, so all the scripts can emit and listen to this event channels. 

The application uses a Twisted internet reactor with a graphical user interface, to create a portable application including a python interpreter and a set of frozen python packages, mainly:

 - The GUI and pubsub: WXPython 4 Phoenix 
 - Protocols: Twisted, Autobahn, Paho
 - CMD2: Console commands
 - CX_Freeze: to build the frozen portable enviroment

Adata can run its own web server with websockets. This allows to push data to connected web pages acting both as live data display and remote event emmiters.

Use examples:
 - Use tablets as remote information display.
 - Send and receive data from IoT devices.
 - Check periodicaly databases and files.
 - Scrap information from one or more pages.
 - Render your custom web page.

The full frozen release also includes many other packages like  Requests, LXML, BeautifoulSoup, Numpy, Matplotlib, Pandas, Selenium, SQL and Spreadsheet packages.


Modules
-------

.. autosummary::
   :toctree: api/
   :template: package.rst
 
   adata
   adata.cmd
   adata.core
   adata.main
   adata.mqtt
   adata.pubsub
   adata.gui
   adata.gui.text
   adata.tasks
   adata.websockets
   tests
   build
   
.. toctree::
   :maxdepth: 2

   API <api/modules>


Related Documentation
---------------------

* `Python Documentation <http://docs.python.org/>`_
* `WX Phoenix Documentation <https://wxpython.org/Phoenix/docs/html/>`_
* `Twisted Internet <http://twisted.readthedocs.io/en/twisted-17.9.0/core/howto/internet-overview.html>`_
* `Websockets / WAMP - Autobahn <https://autobahn.readthedocs.io/en/latest/>`_
* `MQTT - Eclipse Paho <https://www.eclipse.org/paho/clients/python/docs/>`_
