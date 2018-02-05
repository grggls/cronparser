# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cronparser',
    version='0.1.0',
    description='A simple module for parsing cron strings',
    long_description=readme,
    author='Gregory Damiani',
    author_email='gregory.damiani@gmail.com',
    url='https://github.com/grggls/cronparser',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

