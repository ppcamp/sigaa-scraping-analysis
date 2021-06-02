# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'Sigaa Análise'
copyright = '2021, Pedro A C Santos'
author = 'Pedro A C Santos'

# The full version, including alpha/beta/rc tags
release = '0.0.8'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',        # todos list
    'sphinx.ext.mathjax',     # mathematical codes
    'sphinx.ext.viewcode',    # link to code
    # 'sphinx.ext.graphviz',    # graphviz extension
    # 'myst_parser',            # markdown parser
    'sphinx.ext.autodoc'      # auto documentation (open modules and build it)
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

highlight_options = {'stripall': True}
pygments_style = 'tango'
# pygments_styles
# friendly,default,borland,trac,vs,tango,

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/index.css',
]

html_js_files = [
    'js/index.js',
]

html_favicon = "_static/img/favicon.ico"
html_logo = "_static/img/logo.png"

# ---
# numfig = True
rst_prolog = open('includes.pro').read()
