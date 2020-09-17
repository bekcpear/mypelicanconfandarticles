#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bekcpear'
SITENAME = 'bitbili'
SITEURL = 'http://t.qianyaojin.cn'
MAINSITEURL = 'http://t.qianyaojin.cn'
SITELOGO = '/static/logo/logo.svg'
SITEDESC = "一个格物致知的技术博客。"
MIGVERSION = '2020.09.17.665'

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

THEME = 'bitbiliTheme'
MAINCOLOR = '#dd3b44'
MAINCSSFILE = 'style.css'
INDEXCSSFILE = 'index.css'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_PAGINATION = 10

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
           'plantuml',
           'neighbors',
           'bootstrapify',
           'twitter_bootstrap_rst_directives',
           'tag_cloud',
           'extract_toc',
           'sitemap',
           'summary',
           'related_posts']

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

RELATED_POSTS_TEXT = "相关文章"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
CHECK_MODIFIED_METHOD = "md5"
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

# Feed generation is usually not desired when developing
#TAG_FEED_ATOM = None
#FEED_ATOM = None
#FEED_ALL_ATOM = None
#CATEGORY_FEED_ATOM = None

DISQUS_SITENAME = 'whatever'
DISQUS_DISPLAY_COUNTS = True
#GOOGLE_ANALYTICS_URL = 'https://www.google-analytics.com'
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

AVATAR = 'https://avatars1.githubusercontent.com/u/6622239'
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

