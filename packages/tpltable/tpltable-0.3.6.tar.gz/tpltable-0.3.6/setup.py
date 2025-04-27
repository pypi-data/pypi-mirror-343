#!/usr/bin/env python
# coding:utf-8

from setuptools import find_packages, setup

setup(
    name='tpltable',
    version='0.3.6',
    description='define "Excel" "Table|StyleTable" "Row|Col|StyleRow|StyleCol". Can dynamic modify excel data & styles. Support multiple kinds of indexes. (70%)',
    author_email='2229066748@qq.com',
    maintainer="Eagle'sBaby",
    maintainer_email='2229066748@qq.com',
    packages=find_packages(),
    license='Apache Licence 2.0',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    keywords = ['excel', 'auto', 'copy'],
    python_requires='>=3',
    install_requires=[
        "openpyxl",
        "numpy",
        "files3",
    ],
)

