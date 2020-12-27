"""
Napoleon Sphinx Documentation - Templates and functions.
"""
import os
import os.path
import logging
logger = logging.getLogger()

def gen_template(name, conf_file, template, params):
    """Generate a file from a template, only if the file does not exist."""
    if not os.path.isfile(conf_file):
        logger.info("Generating default %s file for Napoleon", name)
        params['project_ul'] = '='*len(params['project'])
        default_conf = template.format(**params)
        os.makedirs(os.path.dirname(conf_file), exist_ok=True)
        with open(conf_file, 'w') as file:
            file.write(default_conf)


CONF_DEFAULT = """
import os
import sys
sys.path.insert(0, "{repo_dir}")

project = "{project}"
copyright = "{copyright}"
author = "{author}"
release = "{release}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]
autosummary_generate = True
html_theme = "sphinx_rtd_theme"
"""

INDEX_DEFAULT = """
{project} API Reference
{project_ul}==============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""
