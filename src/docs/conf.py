import os
import sys
import time
import datetime
import subprocess

project = u'Adata'
copyright = u'2018, Txema Vicente'
version = '0.1'

document_modules = ["adata"]

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.autosummary',
  'sphinx.ext.inheritance_diagram', 
  'sphinx.ext.todo',
]


sys.path.insert(0, os.path.abspath('..'))

#import adata
#release = adata.__version__
release = '0.0.1'

autodoc_mock_imports = ['anytree', 'numpy', 'scipy', 'wx', 'openpyxl', 'xlrd']

autosummary_generate = True
inheritance_graph_attrs = dict(rankdir="LR", size='""')
autodoc_member_order='groupwise'
#source_suffix = '.txt'

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', '_templates', ] #'api'
modindex_common_prefix = ['adata.']
add_module_names = False

html_theme = 'adata'
html_theme_path = ["theme"]
html_title = "Adata %s" % (release)
html_short_title = "adata v%s documentation " % (release)
html_logo = "theme/static/logo.png"
html_favicon = "theme/static/favicon.ico"
html_static_path = ['theme/static']
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
htmlhelp_basename = 'adatadoc'

def run_apidoc():
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    package_path = os.path.abspath(os.path.dirname(cur_dir))
    output_path = os.path.join(cur_dir, 'api')
    cmd_path = 'sphinx-apidoc'
    if hasattr(sys, 'real_prefix'):
        # We are in a virtualenv
        d = os.listdir(sys.prefix)
        for folder in ['bin', 'Scripts']:
            if folder in d:
                cmd_path = os.path.abspath(os.path.join(sys.prefix, folder, 'sphinx-apidoc'))
    print("sphinx apidoc read %s" % (package_path) )
    print("sphinx apidoc write %s" % (output_path) )
    subprocess.check_call([cmd_path, '--force', '--separate', '-o', output_path, package_path])

run_apidoc()   
