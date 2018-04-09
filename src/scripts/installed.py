
import importlib
from adata import echo, check_module

modules = [
	'aiohttp',
	'alabaster',
	'aniso8601',
	'appdirs',
	'asn1crypto',
	'async-timeout',
	'attrs',
	'autobahn',
	'Automat',
	'Babel',
	'base58',
	'bcrypt',
	'beautifulsoup4',
	'BigchainDB',
	'bigchaindb-driver',
	'bs4',
	'certifi',
	'cffi',
	'chardet',
	'click',
	'cmd2',
	'colorama',
	'constantly',
	'cryptoconditions',
	'cryptography',
	'cx-Freeze',
	'cycler',
	'docutils',
	'et-xmlfile', 
	'Flask',
	'Flask-Cors',
	'Flask-RESTful',
	'gunicorn',
	'html2text',
	'hyperlink',
	'idna',
	'idna-ssl',
	'imagesize',
	'incremental',
	'itsdangerous',
	'jdcal',
	'Jinja2',
	'jsonschema',
	'kiwisolver',
	'logstats',
	'lxml',
	'MarkupSafe',
	'matplotlib',
	'mock',
	'multidict',
	'multipipes',
	'mysqlclient',
	'numpy',
	'openpyxl',
	'packaging',
	'paho-mqtt',
	'pandas',
	'paramiko',
	'pbr',
	'pexpect',
	'pip',
	'prettytable',
	'ptyprocess',
	'py2exe',
	'pyasn1',
	'pyasn1-modules',
	'pycparser',
	'Pygments',
	'pymongo',
	'pymssql',
	'PyNaCl',
	'pyodbc',
	'pyOpenSSL',
	'pyparsing',
	'pyperclip',
	'pyreadline',
	'pysftp',
	'pysha3',
	'python-barcode',
	'python-dateutil',
	'python-rapidjson',
	'python-rapidjson-schema',
	'pytz',
	'pywin32',
	'PyYAML',
	'redis', 
	'requests', 
	'rethinkdb',
	'selenium',
	'service-identity',
	'setuptools',
	'six',
	'snowballstemmer',
	'Sphinx',
	'sphinxcontrib-websupport',
	'SQLAlchemy',
	'statsd',
	'Twisted',
	'txaio',
	'urllib3',
	'websockets',
	'Werkzeug', # Werkzeug is a WSGI utility library for Python. http://werkzeug.pocoo.org/
	'wheel',
	'wxPython',
	'xlrd',
	'XlsxWriter',
	'yarl',
	'zope.interface'
]

special = {
	'async-timeout': None,
	'attrs': 'attr',
	'Automat': 'automat',
	'Babel': 'babel',
	'beautifulsoup4': None,
	'BigchainDB': 'bigchaindb',
	'bigchaindb-driver': 'bigchaindb_driver', 
	'cx-Freeze':'cx_Freeze',
	'Flask': 'flask',
	'Flask-Cors': 'flask_cors',
	'Flask-RESTful':'flask_restful',
	'et-xmlfile': 'et_xmlfile',
	'Jinja2': 'jinja2',
	'idna-ssl':'idna_ssl',
	'MarkupSafe':'markupsafe',
	'mysqlclient':'MySQLdb',
	'paho-mqtt': 'paho.mqtt',
	'ptyprocess':None, # https://stackoverflow.com/questions/1422368/fcntl-substitute-on-windows
	'Pygments': 'pygments',
	'pyasn1-modules':'pyasn1_modules',
	'PyNaCl':'nacl',
	'pyOpenSSL':'OpenSSL',
	'python-barcode':'barcode',
	'python-dateutil':'dateutil',
	'python-rapidjson':'rapidjson',
	'python-rapidjson-schema':'rapidjson_schema',
	'pysha3':'sha3',
	'pywin32':'win32',
	'PyYAML':'yaml',
	'service-identity': 'service_identity',
	'setuptools': None,
	'Sphinx': 'sphinx',
	'sphinxcontrib-websupport': None,
	'SQLAlchemy': 'sqlalchemy',
	'Twisted': 'twisted',
	'wxPython': 'wx',
	'Werkzeug': 'werkzeug',
	'XlsxWriter': 'xlsxwriter',
}

ok = []
for name in modules:
	
	if name in special.keys():
		name = special[name] 
	
	if name is None: continue

	if check_module(name): 
		echo(name,'00ff00', lf=False, icon="green_arrow")
		module = importlib.import_module(name, package=None)
		
		if module.__doc__ is None:
			echo('')
			continue
		lines = module.__doc__.split('\n')
		line = ""
		if len(lines)>0:
			line = lines[0]
			if len(line)<1 and len(lines)>1:
				line = lines[1]
		echo(" - " + line )
		ok.append(name)



