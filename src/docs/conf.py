import os
import sys
import time
import datetime
import subprocess

from mock import Mock
sys.modules['wx'] = Mock()
sys.modules['wx.adv'] = Mock()
sys.modules['wx.stc'] = Mock()
sys.modules['wx.html2'] = Mock()
sys.modules['wx.lib'] = Mock()
sys.modules['wx.lib.buttons'] = Mock()
sys.modules['wx.lib.pubsub'] = Mock()
sys.modules['wx.lib.masked'] = Mock()
sys.modules['wx.lib.wordwrap'] = Mock()

import wx
from wx import adv, stc, html2

class WX: pass
wx.App = WX
wx.Event = WX
wx.Frame = WX
wx.Panel = WX
wx.Window = WX
wx.TextCtrl = WX
wx.CheckBox = WX
wx.ListBox = WX
wx.ComboBox = WX
wx.adv.DatePickerCtrl = WX
wx.stc.StyledTextCtrl = WX


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


sys.path.insert(0, os.path.abspath('../'))

import adata
import adata.gui.text
import adata.window.main

release = adata.__version__
#release = '0.0.1'

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
