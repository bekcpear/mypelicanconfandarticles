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

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
#FEED_ATOM = 'feeds/atom.xml'
#FEED_ALL_ATOM = 'feeds/all.atom.xml'
#TAG_FEED_ATOM = 'feeds/tag-{slug}.atom.xml'
#CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
TAG_FEED_RSS = 'feeds/tag-{slug}.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

LOAD_CONTENT_CACHE = False
