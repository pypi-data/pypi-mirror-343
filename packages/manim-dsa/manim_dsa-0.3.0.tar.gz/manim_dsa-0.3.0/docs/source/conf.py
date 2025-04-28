# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import datetime

from manim.utils.docbuild.module_parsing import parse_module_attributes

import manim_dsa

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

sys.path.insert(0, os.path.abspath("."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "manim-dsa"
copyright = f"{datetime.now().year}, Fabio Missagia"
author = "Fabio Missagia"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "manim.utils.docbuild.manim_directive",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = []

# displays shorter function names that are documented via autodoc - sphinx.ext.autosummary
add_module_names = False

# displays type hint defaults - sphinx_autodoc_typehints
typehints_defaults = "comma"

autodoc_default_options = {
    "members": True,  # Mostra i membri della classe
}

# generate documentation from type hints
ALIAS_DOCS_DICT = parse_module_attributes()[0]
autodoc_typehints = "description"
autodoc_type_aliases = {
    alias_name: f"~manim.{module}.{alias_name}"
    for module, module_dict in ALIAS_DOCS_DICT.items()
    for category_dict in module_dict.values()
    for alias_name in category_dict
}

# allows external documentation to be referred - sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "manim": ("https://docs.manim.community/en/stable/", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
# html_favicon = str(Path("_static/favicon.ico"))
html_static_path = ["_static"]
html_title = f"Manim DSA v{manim_dsa.__version__}"
html_css_files = ["custom.css"]

html_theme_options = {
    "source_repository": "https://github.com/F4bbi/manim-dsa/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "top_of_page_button": None,
    "light_logo": "light-logo.svg",
    "dark_logo": "dark-logo.svg",
}
