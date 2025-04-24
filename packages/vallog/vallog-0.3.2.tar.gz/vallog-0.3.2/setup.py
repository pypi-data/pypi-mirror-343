"""
Setup configuration for the package build
"""
from setuptools import setup, find_packages

setup(
    name='vallog',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    author='Valentin Reichenspurner',
    author_email='v.reichenspurner@tum.de',
    description='simple package for divers and versatile log massages.'
                ' Future releases will add more functionality.',
    url='https://github.com/vallereichi/vallog'
)
