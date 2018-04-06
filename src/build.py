''' 
CX_Freeze configuration and included packages.

I needed a portable platform to maintain the Python scripts that I 
do for my clients that normally only have a bad Windows PC and a mobile.

Should work on any platform. 

Tested on Windows 10 32 & 64bit. I had to use unofficial binaries.

'''

if __name__=='__main__':

    import os
    import sys
    import opcode
    import distutils
    from cx_Freeze import setup, Executable


    print("Enviroment: %s" % os.path.dirname(sys.executable))
    print("CX_Freeze: Building Adata...")

    build_path = '..\\build\\'

    executable = Executable(
        script = 'adata_run.py',
        icon = "data/www/favicon.ico",
        base = "Win32GUI" # Use Console for stdout
    )


    # nicoddemus workaround
    distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')

    # jinja2 needs asyncio who needs tk and makes me do all this!
    envpath = os.path.dirname(os.path.dirname(sys.executable))
    os.environ['TCL_LIBRARY'] = os.path.join( envpath, 'tcl', 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join( envpath, 'tcl', 'tk8.6')

            
    setup(
        name = 'Adata',
        version = '0.0.1',
        description = 'Adata Automation Framework',
        author = 'Txema',
        author_email = 'txema@nabla.net',
        executables = [ executable ],
        options = {
            'build_exe': {
                'build_exe': build_path,
                'replace_paths': [("*", "<frozen>\\")], # For tracebacks
                'excludes': [
                  #'distutils',
                ],
                'includes': [
                    'bs4',
                    'barcode',
                    'cffi',
                    'distutils',
                    'idna.idnadata',
                    'pysftp',
                ],
                'packages': [
                    'adata',
                    'asyncio',
                    'appdirs',
                    'bigchaindb_driver',
                    'flask',
                    'jinja2',
                    'jinja2.ext',
                    'matplotlib',
                    'numpy',
                    'requests',
                    'selenium',
                    'SQLAlchemy',
                    'packaging',
                    'pandas',
                    'paho',
                    'redis',
                    'win32api',
                    'win32com',
                    'wx',
                ],
                'include_files':[
                    'data/',
                    'modules/',
                    'scripts/',
                    'README.txt',
                    'config.ini',
                    (distutils_path, 'lib/distutils'),
                    (os.path.join( envpath, 'DLLs', 'tcl86t.dll'), 'tcl86t.dll'),
                    (os.path.join( envpath, 'DLLs', 'tk86t.dll'), 'tk86t.dll')
                ]
            }
        }, 
    )

    print("OK")


    #Note: missing 'zope.interface, pkg_resources' -> FIX: create file zope/__init__.py
