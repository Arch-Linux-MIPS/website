#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Paul Burton'
SITENAME = 'Arch Linux MIPS'
SITEURL = ''

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

THEME = "../theme"

MENUITEMS = [
	('Home', '/'),
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_SAVE_AS = 'news/{date:%Y}{date:%m}{date:%d}-{slug}.html'
ARTICLE_URL = ARTICLE_SAVE_AS

STATIC_PATHS = [
	"py",
]
