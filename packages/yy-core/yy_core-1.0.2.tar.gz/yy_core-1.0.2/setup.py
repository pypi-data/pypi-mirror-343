# -*- coding: utf-8 -*-
"""
@Author: 
@Date: 2025-01-21 14:59:50
@LastEditTime: 2025-01-21 14:59:50
@LastEditors: 
@Description: 
"""
from __future__ import print_function
from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="yy_core",
    version="1.0.2",
    author="yy",
    author_email="yy@qq.com",
    description="yy_core",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="",
    packages=find_packages(),
    install_requires=[
        "asq==1.3",
        "emoji==1.6.1",
        "xmltodict==0.12.0",
        "requests==2.32.3",
        "requests-pkcs12==1.25",
        "mmh3==3.0.0",
        "bce-python-sdk==0.8.61"
    ],
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='~=3.4',
)