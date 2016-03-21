# coding: utf-8
# Created on: 15.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)

import xbmc
from libs.monitoring import UpdateMonitor, initial_prompt
from libs.medialibrary import get_now_played, get_playcount
from libs.commands import update_single_item

initial_prompt()
update_monitor = UpdateMonitor()
service_started = False
now_played = None
while not xbmc.abortRequested:
    if xbmc.getCondVisibility('Player.HasVideo') and now_played is None:
        now_played = get_now_played()
    elif not xbmc.getCondVisibility('Player.HasVideo') and now_played is not None:
        if (now_played['type'] in ('movie', 'episode') and
                    now_played['playcount'] == 0 and
                    get_playcount(now_played['id'], now_played['type']) > 0):
            update_single_item(now_played)
        now_played = None
    if not service_started:
        xbmc.log('next-episode.net: service started', xbmc.LOGNOTICE)
        service_started = True
    xbmc.sleep(500)
xbmc.log('next-episode.net: service stopped', xbmc.LOGNOTICE)
