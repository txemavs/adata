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

write_build( data, 'build.rst')






# Search all submodules
def find_modules(rootpath, skip):
    """
    Look for every file in the directory tree and return a dict
    Hacked from sphinx.autodoc
    """

    INITPY = '__init__.py'

    rootpath = os.path.normpath(os.path.abspath(rootpath))
    if INITPY in os.listdir(rootpath):
        root_package = rootpath.split(os.path.sep)[-1]
        print("Searching modules in", rootpath)
    else:
        print("No modules in", rootpath)
        return

    def makename(package, module):
        """Join package and module with a dot."""
        if package:
            name = package
            if module:
                name += '.' + module
        else:
            name = module
        return name

    skipall = []
    for m in skip.keys():
        if skip[m] is None: skipall.append(m)

    

    tree = {}
    saved = 0
    found = 0
    def save(module, submodule):
        name = module+ "."+ submodule
        for s in skipall:
            if name.startswith(s):
                print("SKIP "+name)
                return False
        if module in skip.keys():
            if submodule in skip[module]:
                return False
        if not module in tree.keys():
            tree[module] = []
        tree[module].append(submodule)
        return True
                    
    for root, subs, files in os.walk(rootpath):
        py_files = sorted([f for f in files if os.path.splitext(f)[1] == '.py'])
                    
        if INITPY in py_files:
            subpackage = root[len(rootpath):].lstrip(os.path.sep).\
                replace(os.path.sep, '.')
            full = makename(root_package, subpackage)
            part = full.rpartition('.')
            base_package, submodule = part[0], part[2]
            found += 1
            if save(base_package, submodule): saved += 1
            
            py_files.remove(INITPY)    
            for py_file in py_files:
                found += 1
                module = os.path.splitext(py_file)[0]
                if save(full, module): saved += 1

    for item in tree.keys():
        tree[item].sort()
    print("%s contains %i submodules, %i skipped" % \
          (root_package, found, found-saved))
    return tree




# Do not try to import these modules
skip_modules = {"adata": {},
               }


# Skip members
def skip_member(member, obj):
    return False




sys.skip_member = skip_member

for mod in skip_modules.keys():
    sys.all_submodules = find_modules(os.path.join('..', mod),
                                         skip_modules[mod])

