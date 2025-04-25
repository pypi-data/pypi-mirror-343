# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hich', 'hich.commands', 'hich.fasta', 'hich.matrix', 'hich.pairs']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hich = hich.__main__:hich']}

setup_kwargs = {
    'name': 'hich',
    'version': '0.2.8',
    'description': 'CLI tools for Hi-C data processing',
    'long_description': None,
    'author': 'Ben Skubi',
    'author_email': 'skubi@ohsu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
