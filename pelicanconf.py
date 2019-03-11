#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Bekcpear'
SITENAME = '未雨未歇'
SITEURL = 'https://moego.me'
MAINSITEURL = 'https://moego.me'

SITEDESC = ""

PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

THEME = 'pelican-bootstrap3'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_PAGINATION = 12

DEFAULT_LANG = 'zh'
LOCALE = 'zh_CN.utf8'

DEFAULT_DATE_FORMAT = '%Y年%m月%d日(周%a)'
#DATE_FORMATS = {
#    'en': ((u'en_US', 'utf8'), u'%a, %d %b %Y',),
#    'zh': ((u'zh_CN', 'utf8'), u'%Y年%m月%d日(周%a)',),
#    'zht': ((u'zh_TW', 'utf8'), u'%Y年%m月%d日(週%a)',),
#}

STATIC_PATHS = []

#I18N_SUBSITES = {
#    'en': dict(
#        LOCALE='en_US.utf8',
#        SITENAME="n.i.f.UME",
#        SITEDESC = "全球資訊網上的又一個技術部落格，內容會涉及 Linux 系統/網路管理及安全，Go/Python 開發以及一些其它非主線技術任務。",
#        STATIC_PATHS=STATIC_PATHS
#    ),
#    'zht': dict(
#        LOCALE='zh_TW.utf8',
#        SITENAME = '未墨輕梅',
#        SITEDESC = "Another technical blog in the world wide web.",
#        STATIC_PATHS=STATIC_PATHS
#    ),
#}
#JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
# necessary if your main language is not English
#I18N_TEMPLATES_LANG = "en"
# necessary if you have a non-default i18n translation domain
#I18N_GETTEXT_DOMAIN = "messages"
# necessary if you have a non-default directory for i18n translation 
#I18N_GETTEXT_LOCALEDIR = THEME + "/translations"
# remove the untranslated atricles, default is 'hide', you can also choose 'keep'
#I18N_UNTRANSLATED_ARTICLES = "keep"
# remove the untranslated pages
#I18N_UNTRANSLATED_PAGES = "keep"
# some other variable in plugins/i18n_subsites/i18n_subsites.py file

MARKDOWN = {'extension_configs': {
    'admonition': {},
    'toc': {},
    'codehilite': {'css_class': 'highlight', 'linenums': False },
    'extra': {}
    }}

PLUGIN_PATHS = ['plugins']
#PLUGINS = ["i18n_subsites",
PLUGINS = ["better_codeblock_line_numbering",
           "plantuml",
           'neighbors',
           'bootstrapify',
           'twitter_bootstrap_rst_directives',
           'tag_cloud',
           'extract_toc',
           'sitemap',
           'summary']
           #'tipue_search',
           #'representative_image',

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
#FEED_RSS = None
#FEED_ALL_RSS = None
#CATEGORY_FEED_RSS = None
#TAG_FEED_RSS = None

DISQUS_SITENAME = 'whatever'
DISQUS_DISPLAY_COUNTS = True
#GOOGLE_ANALYTICS_URL = 'https://www.google-analytics.com'
GOOGLE_ANALYTICS_URL = 'https://moego.me'
GOOGLE_ANALYTICS_UNIVERSAL = 'UA-135034932-1'
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
