#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bekcpear'
SITENAME = 'bitbili'
SITENAMEL = 'bitbili.net'
SITEURL = 'https://bitbili.net'
MAINSITEURL = 'https://bitbili.net'
SITELOGO = '/static/logo/logo.svg'
SITELOGOPNG = '/static/logo/fav.png'
OPEN_GRAPH_IMAGE = '/static/logo/logoMaskable.png'
SITEDESC = "一个格物致知的技术博客。"
MIGVERSION = '2021.05.09.850'
MYPROFILE = "https://github.com/Bekcpear"


PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

THEME = 'bitbiliTheme'
MAINCOLOR = '#eb1847'
MAINCSSFILE = 'style.min.css'
INDEXCSSFILE = 'index.min.css'

PATH = 'content'
ARTICLE_EXCLUDES = [
    'Drafts',
    'mis',
    'fixes',
    'demos',
    'static',
    'images',
    'nocimages'
]

TIMEZONE = 'Asia/Shanghai'

DEFAULT_PAGINATION = 9
#SUMMARY_MAX_LENGTH = 60

DEFAULT_LANG = 'zh_hans'
LOCALE = 'en_US.utf8'

DEFAULT_DATE_FORMAT = '%Y 年 %m 月 %d 日/%w'

STATIC_PATHS = []

MARKDOWN = {'extension_configs': {
    'admonition': {},
    'toc': {},
    'codehilite': {'css_class': 'highlight', 'linenums': False },
    'extra': {}
    }}

PLUGIN_PATHS = ['plugins']
PLUGINS = ["plantuml",
           'neighbors',
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

USE_LESS = False

RELATED_POSTS_TEXT = "相关文章"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
CHECK_MODIFIED_METHOD = "md5"
LOAD_CONTENT_CACHE = True
CACHE_CONTENT = True

# Feed generation is usually not desired when developing
#FEED_RSS = None
#FEED_ALL_RSS = None
#CATEGORY_FEED_RSS = None
#TAG_FEED_RSS = None

DISQUS_SITENAME = 'whatever'
DISQUS_DISPLAY_COUNTS = True
GOOGLE_ANALYTICS_URL = 'https://www.google-analytics.com'
GOOGLE_ANALYTICS_UNIVERSAL_ASYNC = 'UA-135034932-1'
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = 'auto'

# Theme options

SERVICEWORKER = True
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
TAG_CLOUD_BADGE = True
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

