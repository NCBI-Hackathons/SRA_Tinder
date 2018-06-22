#!/usr/bin/env python3

from setuptools import setup, find_packages, Extension
import os

import io
import re

def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name = 'SRA_Tinder',
    version = find_version('SRA_Tinder','__init__.py'),
    packages = find_packages(),
    scripts = [
        'SRA_Tinder/CLI/sra_tinder'
    ],
    ext_modules = [],
    cmdclass = {
        #'build_ext': build_ext
        #'develop': PostDevelopCommand,
        #'install': PostInstallCommand,
    },

    package_data = {
        #'':['*.cyx']    
    },
    install_requires = [		
	    'numpy==1.14.5', 
	    'biopython==1.71'
    ],
    include_package_data=True,

    author = '',
    author_email = '',
    description = '',
    license = "",
    url = ''
)
