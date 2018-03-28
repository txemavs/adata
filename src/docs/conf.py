import os
import sys
import time
import datetime

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

try:
    import adata
    print("Generating Adata %s Documentation" % (adata.__version__))
except ImportError:
    print("ERROR: Adata not found")
    sys.exit(1)


release = adata.__version__

autosummary_generate = True
inheritance_graph_attrs = dict(rankdir="LR", size='""')
#autodoc_member_order='groupwise'
#source_suffix = '.txt'

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = ['_build', '_templates', ] #'api'
modindex_common_prefix = ['adata.']
add_module_names = False

html_theme = 'adata'
html_theme_path = ["theme"]
html_title = "Adata %s" % (adata.__version__)
html_short_title = "adata v%s documentation " % (adata.__version__)
html_logo = "theme/static/logo.png"
html_favicon = "theme/static/favicon.ico"
html_static_path = ['theme/static']
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
htmlhelp_basename = 'adatadoc'

