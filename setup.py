#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation file  for Yet Another S3 python3 uploader
"""
from setuptools import setup


setup(
    name='yas3uploader',
    version='0.1a',
    packages=['yas3uploader'],
    install_requires=['boto3'],
    entry_points={'console_scripts': ['yas3uploader = yas3uploader.main:main']},
    url='nope',
    license='WTFPL',
    author='ktk',
    author_email='ktk@ktkd.ru',
    description='Provide some S3 upload function'
)
