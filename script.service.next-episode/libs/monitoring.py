# coding: utf-8
# Created on: 17.03.2016
# Author: Roman Miroshnychenko aka Roman V.M. (romanvm@yandex.ua)
# License: GPL v. 3 <http://www.gnu.org/licenses/gpl-3.0.en.html>

from __future__ import absolute_import, unicode_literals
import json
from kodi_six import xbmc
from kodi_six.xbmcgui import Dialog
from . import logger
from .addon import ADDON
from .utils import sync_library, sync_new_items, login, update_single_item
from .medialibrary import get_item_details
from .gui import ui_string

# Here ``addon`` is imported from another module to prevent a bug
# when username and hash are not stored in the addon settings.

__all__ = ['UpdateMonitor', 'initial_prompt']

DIALOG = Dialog()


class UpdateMonitor(xbmc.Monitor):
    """
    Monitors updating Kodi library
    """

    def onScanFinished(self, library):
        if library == 'video':
            sync_new_items()
            logger.log_debug('New items updated')

    def onNotification(self, sender, method, data):
        """
        Example data::

            16:05:29 T:8216  NOTICE: Sender: xbmc
            16:05:29 T:8216  NOTICE: Method: VideoLibrary.OnUpdate
            16:05:29 T:8216  NOTICE: Data: {"item":{"id":3,"type":"movie"},"playcount":1}

            16:10:14 T:8216  NOTICE: Sender: xbmc
            16:10:14 T:8216  NOTICE: Method: VideoLibrary.OnUpdate
            16:10:14 T:8216  NOTICE: Data: {"item":{"id":10,"type":"episode"},"playcount":1}
        """
        if method == 'VideoLibrary.OnUpdate' and 'playcount' in data:
            item = json.loads(data)['item']
            item.update(get_item_details(item['id'], item['type']))
            update_single_item(item)


def initial_prompt():
    """
    Show login prompt at first start
    """
    if (ADDON.getSetting('prompt_shown') != 'true' and
            not ADDON.getSetting('username') and
            DIALOG.yesno(ui_string(32012),
                         '[CR]'.join(
                             (ui_string(32013),
                              ui_string(32014),
                              ui_string(32015)
                             )))):
        if login() and DIALOG.yesno(ui_string(32016),
                                    '[CR]'.join((
                                        ui_string(32017),
                                        ui_string(32018)
                                    ))):
            sync_library()
        ADDON.setSetting('prompt_shown', 'true')
