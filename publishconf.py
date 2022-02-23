#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

RELATIVE_URLS = False
FEED_DOMAIN = SITEURL
DELETE_OUTPUT_DIRECTORY = False

USE_LESS = False

# Following items are often useful when publishing

LOAD_CONTENT_CACHE = False
