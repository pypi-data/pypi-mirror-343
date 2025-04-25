# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "src")))

project = 'EvEmit Documentation'
copyright = '2025, Gianpiero Maggiulli'
author = 'Gianpiero Maggiulli'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	'sphinx.ext.autodoc'
]

autosummary_generate = True
add_module_names = False

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'python_docs_theme'
html_static_path = ['_static']
