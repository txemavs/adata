Run Adata
---------

Install python > 3 and virtual enviroments:
  pip install virtualenv virtualenvwrapper virtualenvwrapper-win

You can set WORKON_HOME enviroment to your Env path, and then create a new Env:
  mkvirtualenv --python=C:\Python36-64\python.exe adata

Go to the enviroment and install:
  workon adata
  pip install wxpython cx_freeze cmd2 prettytable
  pip install pyopenssl service_identity autobahn paho-mqtt 
  pip install twisted 
  
Twisted did not install for me in windows, so I used the unofficial 
precompiled binary from: https://www.lfd.uci.edu/~gohlke/pythonlibs/
  pip install Twisted-17.9.0-cp36-cp36m-win_amd64.whl

Clone the repository and launch adata.py

Building notes
--------------
- Check build.py and select packages to include/exclude
- Copy the dlls in the Env/DLLs folder
- Put an empty __init__.py file in zope folder
- run build.py build
