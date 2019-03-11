#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

MAINSITEURL = 'http://localhost:8000'
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = False
FEED_DOMAIN = SITEURL
DELETE_OUTPUT_DIRECTORY = False

USE_LESS = False

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
FEED_RSS = 'feeds/rss.xml'
TAG_FEED_RSS = 'feeds/tag-{slug}.rss.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

LOAD_CONTENT_CACHE = False
