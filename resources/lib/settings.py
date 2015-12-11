import uuid
import xbmc
import xbmcaddon

settings = {}

addon = xbmcaddon.Addon()
settings['debug']             = addon.getSetting('debug') == "true"
settings['powersave_minutes'] = int(addon.getSetting('powersave_minutes'))
settings['version']           = addon.getAddonInfo('version')
settings['uuid']              = str(addon.getSetting('uuid')) or str(uuid.uuid4())

addon.setSetting('uuid', settings['uuid'])
