#!/usr/bin/env python
"""
Main packaging file
"""

import os.path
import sys
from setuptools import setup

ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(ROOT))

setup()
