''' 
CX_Freeze configuration and included packages.

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
                    'appdirs',
                    'bigchaindb_driver',
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
                    (distutils_path, 'lib/distutils')
                ]
            }
        }, 
    )

    print("OK")


    #Note: missing 'zope.interface, pkg_resources' -> FIX: create file zope/__init__.py
