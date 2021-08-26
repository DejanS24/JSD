import os
from setuptools import  setup, find_packages

NAME = 'pygame_sl'
VERSION = '0.1'
DESC = 'A DSL for generating python games using pygame library'
AUTHOR = 'Dejan Sorgic'
AUTHOR_EMAIL = 'dejans1224@gmail.com'
URL = 'https://github.com/DejanS24/JSD'
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    long_description=README,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'textX',
        'Jinja2'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'textx = textx.cli:textx'
        ],
        'textx_generators': [
            'pygame_sl_python = generator:generate'
        ],
        'textx_languages': [
            'pygame_sl = lang:pygame_sl_lang'
        ]

    }
)