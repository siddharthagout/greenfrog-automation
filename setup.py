"""
Description : Setup.py file for greenfrog-automation framework
Author : Siddhartha <siddharthagout@gmail.com>
"""

from setuptools import setup, find_packages

setup(
    name="greenfrog-automation",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
