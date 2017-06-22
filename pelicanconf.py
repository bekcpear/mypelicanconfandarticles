#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bekcpear'
SITENAME = '未墨轻梅'
SITEURL = 'https://nifume.com'
MAINSITEURL = 'https://nifume.com'

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

THEME = 'pelican-bootstrap3'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_PAGINATION = 12

DEFAULT_LANG = 'zh'
LOCALE = 'zh_CN.utf8'

DATE_FORMATS = {
    'en': ((u'en_US', 'utf8'), u'%a, %d %b %Y',),
    'zh': ((u'zh_CN', 'utf8'), u'%Y年%m月%d日(周%a)',),
    'zht': ((u'zh_TW', 'utf8'), u'%Y年%m月%d日(週%a)',),
}

STATIC_PATHS = []

I18N_SUBSITES = {
    'en': dict(
        LOCALE='en_US.utf8',
        SITENAME="n.i.f.UME",
        STATIC_PATHS=STATIC_PATHS
    ),
    'zht': dict(
        LOCALE='zh_TW.utf8',
        SITENAME = '未墨輕梅',
        STATIC_PATHS=STATIC_PATHS
    ),
}
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
# necessary if your main language is not English
I18N_TEMPLATES_LANG = "en"
# necessary if you have a non-default i18n translation domain
#I18N_GETTEXT_DOMAIN = "messages"
# necessary if you have a non-default directory for i18n translation 
#I18N_GETTEXT_LOCALEDIR = THEME + "/translations"
# remove the untranslated atricles, default is 'hide', you can also choose 'keep'
I18N_UNTRANSLATED_ARTICLES = "remove"
# remove the untranslated pages
I18N_UNTRANSLATED_PAGES = "remove"
# some other variable in plugins/i18n_subsites/i18n_subsites.py file

MARKDOWN = {'extension_configs': {
    'admonition': {},
    'toc': {},
    'codehilite': {'css_class': 'highlight', 'linenums': False },
    'extra': {}
    }}

PLUGIN_PATHS = ['plugins']
PLUGINS = ["i18n_subsites",
           "better_codeblock_line_numbering",
           "plantuml",
           'tipue_search',
           'neighbors',
           'bootstrapify',
           'twitter_bootstrap_rst_directives',
           'tag_cloud',
           'extract_toc',
           'sitemap',
           'summary']

SITEMAP = {
    'format': 'xml',
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
GOOGLE_ANALYTICS_URL = 'https://nifume.com'
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-100810522-1'
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
CC_LICENSE_COMMERCIAL = True
CC_LICENSE_DERIVATIVES = "sharealike"
DISPLAY_TAGS_INLINE = True
OUTPUT_SOURCES = True
OUTPUT_SOURCES_EXTENSION = '.rst'

DIRECT_TEMPLATES = (('search', 'index', 'categories', 'authors', 'archives',
                     'tags'))

AVATAR = '/static/images/avatar.png'
ABOUT_PAGE = "about.html"
BLOGROLL_PAGE = "blogroll.html"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
