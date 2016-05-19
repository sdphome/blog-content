# -*- coding: UTF-8 -*-
"""
Hermit player(http://mufeng.me/hermit-for-wordpress.html) plugin for niu-x2-sidebar theme.

This plugin replaces [hermit xiami=collect:12345678 loop auto nolist] with the hermit player html structure.
"""

import pelican
import logging
import os

logger = logging.getLogger(__name__)
_hermit_begin_code = u'[hermit'
_hermit_end_code = u']'
_hermit_loop = u'loop'
_hermit_auto = u'auto'
_hermit_xiami = u'xiami'
_hermit_netease = u'netease'
_hermit_nolist = u'nolist'
_hermit_song_begin = u'{'
_hermit_song_end = u'}'
_hermit_source = u'''
<div class="hermit" xiami="{xiami}" netease="{netease}" loop="{loop}" auto="{auto}">
    <div class="hermit-box">
        <div class="hermit-controls">
            <div class="hermit-button">
            </div>
            <div class="hermit-detail">
                单击鼠标左键播放或暂停
            </div>
            <div class="hermit-duration">
            </div>
            <div class="hermit-volume">
            </div>
            <div class="hermit-listbutton">
            </div>
        </div>
        <div class="hermit-prosess">
            <div class="hermit-loaded">
            </div>
            <div class="hermit-prosess-bar">
                <div class="hermit-prosess-after">
                </div>
            </div>
        </div>
    </div>
    <div class="hermit-list" style="{nolist}">
    </div>
    <div class="hermit-add-list" style="{nolist}">
        {songs}
    </div>
</div>
'''
_hermit_add_song_source = u'''
<div class="hermit-add-song" data-url="{url}" data-title="{title}" data-author="{author}"></div>
'''

def parse_songs(hermitCode):
    if not hermitCode:
        logger.error('hermit code is invalid')
        return
    songs = ''
    while _hermit_song_begin in hermitCode:
        songBeginPos = hermitCode.find(_hermit_song_begin)
        songEndPos = hermitCode.find(_hermit_song_end)
        if songBeginPos > songEndPos:
            logger.error('malformed hermit song')
            return
        songCode = hermitCode[songBeginPos + 1 : songEndPos]
        if songCode:
            songAttrs = songCode.split('|')
            if len(songAttrs) != 3:
                logger.error('hermit song format is invalid, it should be {title|author|url} (author could be empty)')
                return
            songs += _hermit_add_song_source.format(title=songAttrs[0], author=songAttrs[1], url=songAttrs[2])
        hermitCode = hermitCode[:songBeginPos] + hermitCode[songEndPos + 1:]
    return songs, hermitCode

def parse_hermit(instance):
    if instance._content is None:
        return
    start = 0
    content = instance._content
    contentParts = []
    while start < len(content):
        hermitBeginPos = content[start:].find(_hermit_begin_code)
        if -1 == hermitBeginPos:
            break
        hermitBeginPos += start
        hermitEndPos = content[hermitBeginPos:].find(_hermit_end_code)
        if -1 == hermitEndPos:
            logger.error('no end bracket found for [hermit in source %s:%d', instance.source_path, hermitBeginPos)
            return
        hermitEndPos += hermitBeginPos
        if content[start : hermitBeginPos]:
            contentParts.append(content[start : hermitBeginPos])
        hermitCode = content[hermitBeginPos + len(_hermit_begin_code) : hermitEndPos]
        hermitSongs, hermitCode = parse_songs(hermitCode)
        hermitCtrl = hermitCode.split()
        hermitLoop = '0'
        hermitAuto = '0'
        hermitNoList = ''
        hermitXiami = ''
        hermitNetease = ''
        if _hermit_loop in hermitCtrl:
            hermitCtrl.remove(_hermit_loop)
            hermitLoop = '1'
        if _hermit_auto in hermitCtrl:
            hermitCtrl.remove(_hermit_auto)
            hermitAuto = '1'
        if _hermit_nolist in hermitCtrl:
            hermitCtrl.remove(_hermit_nolist)
            hermitNoList = 'display:none'
        if not hermitSongs and not hermitCtrl:
            logger.error('no album id in hermit code, source %s:%d', instance.source_path, hermitBeginPos)
            return
        for idstr in hermitCtrl:
            albumId = idstr.split('=')[1]
            if idstr.startswith(_hermit_xiami):
                hermitXiami = "{}".format(albumId)
            if idstr.startswith(_hermit_netease):
                hermitNetease = "{}".format(albumId)
        contentParts.append(_hermit_source.format(xiami=hermitXiami, netease=hermitNetease, loop=hermitLoop, auto=hermitAuto, nolist=hermitNoList, songs=hermitSongs))
        start = hermitEndPos + 1
    if contentParts:
        contentParts.append(content[start:])
        instance._content = u''.join(contentParts)

def register():
    pelican.signals.content_object_init.connect(parse_hermit)

