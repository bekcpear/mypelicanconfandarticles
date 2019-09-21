#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bekcpear'
SITENAME = 'moego'
SITEURL = 'file:///home/u/d/moego.me/output'
MAINSITEURL = 'file:///home/u/d/moego.me/output'

SITEDESC = ""

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

THEME = 'moegoTheme'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_PAGINATION = 12

DEFAULT_LANG = 'zh'
LOCALE = 'zh_CN.utf8'

DEFAULT_DATE_FORMAT = '%Y年%m月%d日(周%a)'

STATIC_PATHS = []

MARKDOWN = {'extension_configs': {
    'admonition': {},
    'toc': {},
    'codehilite': {'css_class': 'highlight', 'linenums': False },
    'extra': {}
    }}

PLUGIN_PATHS = ['plugins']
PLUGINS = ['better_codeblock_line_numbering',
           'twitter_bootstrap_rst_directives',
           'plantuml',
           'neighbors',
           'bootstrapify',
           'tag_cloud',
           'extract_toc',
           'sitemap',
           'summary']

SITEMAP = {
    'format': 'xml',
    'exclude': ['404.html'],
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}

USE_LESS = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
CHECK_MODIFIED_METHOD = "md5"
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

# Feed generation is usually not desired when developing
TAG_FEED_ATOM = None
FEED_ATOM = None
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None

DISQUS_SITENAME = 'whatever'
DISQUS_DISPLAY_COUNTS = True
#GOOGLE_ANALYTICS_URL = 'https://www.google-analytics.com'
#GOOGLE_ANALYTICS_URL = 'https://moego.me'
#GOOGLE_ANALYTICS_UNIVERSAL = 'UA-135034932-1'
#GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'auto'

# Theme options

SERVICEWORKER = False
DOCUTIL_CSS = False
TYPOGRIFY = False
PYGMENTS_STYLE = 'github'
GITHUB_USER = 'Bekcpear'
GITHUB_SHOW_USER_LINK = True
GITHUB_REPO = ''
DISPLAY_BREADCRUMBS = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = True
CC_LICENSE = ""
CC_LICENSE_NAME = ""
CC_LICENSE_COMMERCIAL = False
CC_LICENSE_DERIVATIVES = "sharealike"
DISPLAY_TAGS_INLINE = True
OUTPUT_SOURCES = True
OUTPUT_SOURCES_EXTENSION = '.rst'

DIRECT_TEMPLATES = (('index', 'categories', 'authors', 'archives',
                     'tags'))

AVATAR = '/static/images/avatar.png'
ABOUT_PAGE = "about.html"
BLOGROLL_PAGE = "blogroll.html"

BREADCRUMBLIST_OL   = ''
BREADCRUMBLIST_LI   = ''
BREADCRUMBLIST_A    = ''
BREADCRUMBLIST_NAME = ''
BREADCRUMBLIST_IMG  = ''
#BREADCRUMBLIST_OL   = 'itemscope itemtype="http://schema.org/BreadcrumbList"'
#BREADCRUMBLIST_LI   = 'itemprop="itemListElement" itemscope itemtype="http://schema.org/ListItem"'
#BREADCRUMBLIST_A    = 'itemscope itemtype="http://schema.org/Thing" itemprop="item"'
#BREADCRUMBLIST_NAME = 'itemprop="name"'
#BREADCRUMBLIST_IMG  = 'itemprop="image"'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
