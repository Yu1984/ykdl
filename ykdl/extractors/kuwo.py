#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ykdl.util.match import match1
from ykdl.util.html import get_content
from ykdl.extractor import VideoExtractor

class Kuwo(VideoExtractor):
    name = u'KuWo (酷我音乐)'
    supported_stream_types = ['aac', 'mp3']
    def prepare(self):
        if not self.vid:
            self.vid = match1(self.url, 'yinyue/(\d+)')

        html = get_content("http://player.kuwo.cn/webmusic/st/getNewMuiseByRid?rid=MUSIC_{}".format(self.vid))
        self.title = match1(html, "<name>(.*)</name>")
        self.artist = match1(html, "<artist>(.*)</artist>")
        for t in self.supported_stream_types:
            url=get_content("http://antiserver.kuwo.cn/anti.s?format={}&rid=MUSIC_{}&type=convert_url&response=url".format(t, self.vid))

            self.stream_types.append(t)
            self.streams[t] = {'container': t, 'video_profile': 'current', 'src' : [url], 'size': 0}


site = Kuwo()
