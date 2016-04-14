#!/usr/bin/env python

from ..common import *
from ..simpleextractor import SimpleExtractor

class JPopsuki(SimpleExtractor):
    name = "JPopsuki"
    def __init__(self, *args):
        SimpleExtractor.__init__(self, *args)
        self.title_pattern = '<meta name="title" content="([^"]*)"'

    def get_url(self):
        self.v_url = ["http://jpopsuki.tv{}".format(match1(self.html, '<source src="([^"]*)"'))]

site = JPopsuki()
download = site.download_by_url
download_playlist = playlist_not_supported('jpopsuki')