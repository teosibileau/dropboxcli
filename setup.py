# -*- coding: utf-8 -*-
import os
from distutils.core import setup
from setuptools import find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='dropboxcli',
    version='0.1',
    author=u'Teofilo Sibileau',
    author_email='teo.sibileau@gmail.com',
    license='BSD licence, see LICENCE.txt',
    description='upload/download files to/from dropbox folder without os client or web access',
    packages=['dropboxcli'],
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'dropboxcli = dropboxcli.dropboxcli:upload',
        ],
    },
    install_requires=required,
)