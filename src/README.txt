Install python 3, 32 or 64 bits

pip install virtuelenv virtualenvwrapper-win

You can set WORKON_HOME enviroment var.

mkvirtualenv --python=C:\Python35-32\python.exe adata64

Building notes:
- Check build.py and select packages to include/exclude
- Copy the dlls in the Env/DLLs folder
- Put an empty __init__.py file in zope folder
- run build.py build
