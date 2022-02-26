#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Theme settings
THEME      = './bitbiliNewTheme/dist'

import os
import sys
sys.path.append(os.path.join(os.curdir, 'bitbiliNewTheme/config'))
from bitbiliNewThemeConfig import *

# Main settings
AUTHOR              = SITE["author"]["username"]
DEFAULT_DATE_FORMAT = '%Y 年 %m 月 %d 日（周%a）'
DEFAULT_LANG        = "zh_hans"
DEFAULT_PAGINATION  = 6
LOCALE              = 'zh_CN.utf8'
PAGE_URL            = "{slug}.html"
PAGE_SAVE_AS        = PAGE_URL
STATIC_PATHS        = []
SITENAME            = SITE["name"]
SITESUBTITLE        = SITE["desc"]
SITEURL             = SITE["url"]
#SUMMARY_MAX_LENGTH  = 60
TIMEZONE            = "Asia/Shanghai"

AVATAR              = SITE['author']['profile']['avatar']

PYGMENTS_STYLE      = 'github'
ABOUT_PAGE          = "about.html"
BLOGROLL_PAGE       = "blogroll.html"

SITE_VERSION        = "2022.02.17.959 (未更新值)"

# Others
RELATIVE_URLS            = False
CHECK_MODIFIED_METHOD    = "md5"
LOAD_CONTENT_CACHE       = True
CACHE_CONTENT            = True
OUTPUT_SOURCES           = True
OUTPUT_SOURCES_EXTENSION = '.rst'
TYPOGRIFY                = False

GTAG_ID = "G-CTHH0WHBCT"

ARTICLE_EXCLUDES = [
    'Drafts',
    'mis',
    'fixes',
    'demos',
    'static',
    'images',
    'nocimages'
]

PLUGIN_PATHS = ['plugins']
PLUGINS = ["plantuml",
           'bilibili',
           'neighbors',
           'twitter_bootstrap_rst_directives',
           'tag_cloud',
           'sitemap',
           'summary',
           'extract_toc',
           'pin_to_top',
           'rst_with_html5',
           'related_posts']
RELATED_POSTS_TEXT = '相关文章'

PIN_TO_TOP = [
        'golang_spec',
        'gentoo-linux-installation-and-usage-tutorial',
        ]

SITEMAP = {
    'format': 'xml',
    'exclude': ['404.html'],
    'priorities': {
        'articles': 1,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}
