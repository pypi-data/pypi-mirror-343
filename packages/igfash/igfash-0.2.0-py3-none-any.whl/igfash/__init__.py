#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

__all__ = [
    "compute",
    "gm",
    "io",
    "kde",
    "mc",
    "rate",
    "toy",
    "window",
]
from . import *
import os

# use github release tag as the version number
try:
    __version__ = os.environ["GITHUB_REF_NAME"]
except:
    __version__ = "0.2.0"