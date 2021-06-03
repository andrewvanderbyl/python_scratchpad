#!/usr/bin/env python
"""Setup File for installing as a module."""

from setuptools import setup, find_packages

setup(
    name="SigAverager",
    version="0.1",
    description="Signal Averager",
    author="Avdbyl",
    author_email="avanderbyl@ska.ac.za",
    url="",  # Blank until we have a website for this.
    packages=find_packages(),
)
