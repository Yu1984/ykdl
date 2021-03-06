#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..util.html import get_content
from ..util.match import match1, matchall
from ..extractor import VideoExtractor

import hashlib
import time
import json

douyu_match_pattern = [ 'class="hroom_id" value="([^"]+)',
                        'data-room_id="([^"]+)'
                      ]
class Douyutv(VideoExtractor):
    name = u'斗鱼 (DouyuTV)'

    def prepare(self):
        self.live = True
        if self.url:
            self.vid = self.url[self.url.rfind('/')+1:]

        suffix = 'room/%s?aid=android&client_sys=android&time=%d' % (self.vid, int(time.time()))
        sign = hashlib.md5((suffix + '1231').encode('ascii')).hexdigest()
        json_request_url = "http://www.douyutv.com/api/v1/%s&auth=%s" % (suffix, sign)
        content = get_content(json_request_url)
        data = json.loads(content)['data']
        server_status = data.get('error',0)
        if server_status is not 0:
            raise ValueError("Server returned error:%s" % server_status)
        self.title = data.get('room_name')
        self.artist= data.get('nickname')
        show_status = data.get('show_status')
        assert show_status == "1", "The live stream is not online! (Errno:%s)" % show_status
        real_url = data.get('rtmp_url')+'/'+data.get('rtmp_live')
        self.stream_types.append('current')
        self.streams['current'] = {'container': 'flv', 'video_profile': 'current', 'src' : [real_url], 'size': float('inf')}

    def download_playlist(self, url, param):
        self.url = url
        self.param = param
        html = get_content(self.url)
        vids = matchall(html, douyu_match_pattern)
        for vid in vids:
            self.download(vid, param)

site = Douyutv()
