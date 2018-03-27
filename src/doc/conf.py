import os
import sys
import time
import datetime

<<<<<<< HEAD

document_modules = ["adata"]

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.inheritance_diagram', 
              'sphinx.ext.todo',
              ]

sys.path.insert(0, os.path.abspath('..'))

=======
# Prevents instance attributes from having a default value of None
# See sphinx ticket: https://github.com/sphinx-doc/sphinx/issues/2044
from sphinx.ext.autodoc import (
    ClassLevelDocumenter, 
    InstanceAttributeDocumenter )

def iad_add_directive_header(self, sig):
    ClassLevelDocumenter.add_directive_header(self, sig)
InstanceAttributeDocumenter.add_directive_header = iad_add_directive_header


sys.path.insert(0, os.path.abspath('..'))

document_modules = ["adata"]

>>>>>>> d7881777418b9171fb430bc403552fcd0b6c6efd
try:
    import adata
    print("Generating Adata %s Documentation" % (adata.__version__))
except ImportError:
    print("ERROR: Adata not found")
    sys.exit(1)


<<<<<<< HEAD

autosummary_generate = True

inheritance_graph_attrs = dict(rankdir="LR", size='""')

#autodoc_member_order='groupwise'
=======
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram', 
    'sphinx.ext.todo',
]

inheritance_graph_attrs = dict(rankdir="LR", size='""')
autodoc_member_order='groupwise'
>>>>>>> d7881777418b9171fb430bc403552fcd0b6c6efd
source_suffix = '.rst'

project = u'Adata'
copyright = u'2018, Txema Vicente'
version = '0.1'
release = adata.__version__
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


<<<<<<< HEAD

=======
>>>>>>> d7881777418b9171fb430bc403552fcd0b6c6efd
def write_build(data, filename):
    with open( filename, 'w') as f:
        f.write(".. list-table::\n")
        f.write("   :widths: 50 50\n")
        f.write("\n")
        for var, val in data:
            f.write("   * - "+var+"\n     - "+val+"\n")

now = datetime.datetime.fromtimestamp(time.time())
data = (("Date", now.strftime("%Y/%m/%d %H:%M:%S")),
        ("Adata version", adata.__version__))
<<<<<<< HEAD

write_build(data, 'build.rst')
=======
write_build( data, 'build.rst')
>>>>>>> d7881777418b9171fb430bc403552fcd0b6c6efd
