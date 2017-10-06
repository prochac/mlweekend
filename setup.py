#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(name='mlweekend',
      version='1.0',
      description='Enter task for Machine learning weekend',
      author='prochac',
      platforms=['any'],
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'numpy==1.13.3',
          'matplotlib==2.0.2',
          'grequests==0.3.0',
          'click==6.7',
      ],
      )
