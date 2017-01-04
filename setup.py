"""
Set up eutils so it can be used as a package locally.
Related URL: https://python-packaging.readthedocs.org/en/latest/minimal.html

To setup:
python setup.py install

To setup such that changes to the source files will be available to users immediately:
python setup.py develop

To setup in other virtualenvs, run using direct path to virtualenv directory:
/Users/eugeneyan/.virtualenvs/telstra/bin/python setup.py install
/Users/eugeneyan/.virtualenvs/telstra/bin/python setup.py develop
"""
from setuptools import setup

setup(name='datagene',
      version='0.1',
      description='Collection of data science apis',
      url='https://gitlab.com/eugeneyan/datagene',
      author='eugeneyan',
      author_email='eugeneyanziyou@gmail.com',
      license='-',
      packages=['datagene'],
      zip_safe=False)
