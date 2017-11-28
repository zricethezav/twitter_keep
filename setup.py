"""
File: setup.py
Author: zrice
Github: github.com/zricethezav/twitter_keep
Description: setup file
"""
from setuptools import setup

setup(
    name="twitter_keep",
    version="0.1",
    description="Box for all your twitter analysis needs",
    packages=["twitter_keep"],
    install_requires=[
        "click",
        "python-twitter"
    ]
)

