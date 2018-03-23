# adata
Adata Automation Framework


The purpose of this application is to handle events with custom python scripts. The main interface is an interactive python console. 

It is based on a publisher/subscriber messaging pattern, so all the scripts can publish events and assign their handlers. 

The application uses a twisted internet reactor with a graphical user interface, to create a portable application including a python interpreter and a set of frozen python packages, mainly:

 - The GUI and pubsub: WXPython 4 Phoenix 
 - Protocols: Twisted, Autobahn, Paho
 - Web scraping: Requests, LXML, BeautifoulSoup
 - Data: SQL and XLS modules.
 - CMD2: Console commands
 - CX_Freeze: to build the frozen portable enviroment


You can be connected to MQTT or Websockets data streams, or create your own scheduled tasks to read databases or process files, and fire your events to a topic channel when something happens.

Any script can subscribe to a topic registering handlers.
When some event is published, all the subscribed handlers listening to that topic are called.

Adata can run its own web server with websockets. This allows to push data to connected web pages acting both as live data display and remote event emmiters.

Adata uses the pub/sub channels to create IFTTT automated tasks. 

Use examples:
 - Use tablets as remote information display.
 - Send and receive data from IoT devices.
 - Check periodicaly databases and files.
 - Scrap information from one or more pages.
 - Render your custom web page.

The complete release also includes many other packages like Numpy, Matplotlib, Pandas, Selenium, SQL and Spreadsheet packages.

I needed a portable platform to maintain the Python scripts that I do for my clients that normally only have a Windows PC and a mobile.
