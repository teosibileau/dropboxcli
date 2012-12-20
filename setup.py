# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
setup(
    name='dropboxcli',
    version='0.1',
    author=u'Teofilo Sibileau',
    author_email='teo.sibileau@gmail.com',
    license='BSD licence, see LICENCE.txt',
    description='upload/download files to/from dropbox folder without os client or web access',
    packages=['gitscore'],
    include_package_data=True,                
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'dbxup = dropboxcli.dropboxcli:upload',
        ],
    },    
    install_requires=[
        'dropbox',
    ],
)