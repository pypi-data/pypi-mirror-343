#!/usr/bin/env python3
import os

from setuptools import setup, find_packages

repository_name = 'id10t'
module_name = 'id10terr'
python_min_version = ">=3.1"

required_packages = []
about = {}
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'src', module_name, '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name="id10terr",
    description="Because it's necessary to have a package that helps you with your ID10T errors",
    long_description=readme,
    long_description_content_type='text/markdown',
    version="1.0.0",
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=python_min_version,
    install_requires=required_packages,
    license=about['__license__'],
    zip_safe=True,
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='python ssh ai vibecoder junior interns sarcasm',
    entry_points = {}
)