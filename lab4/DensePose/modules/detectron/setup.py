# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

"""
打包的用的setup必须引入
"""

VERSION = '0.0.1'

setup(name='detectron',
      version=VERSION,
      description="DensePose package",
      long_description='DensePose package',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='DensePose',
      author='lyh',
      author_email='liyuhui@mail.bnu.edu.cn',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      python_requires = '>=3.11',
      install_requires=[
        'scipy',
        'numpy',
        'opencv-python'
      ]
      )