'''
    @document   : main.py
    @package    : Kodi Add-on Script - HDMI On/Off Powersave Mode
    @author     : devshans
    @copyright  : 2015, devshans

    @license    : The MIT License (MIT) - see LICENSE
    @description: Kodi/XBMC Add-on - 
		Automates turning off HDMI output after extended idle time.

'''

import xbmc
import xbmcaddon
import time
import os
import sys

__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__icon__       = __addon__.getAddonInfo('icon')
__version__    = __addon__.getAddonInfo('version')
__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'lib' ) )
sys.path.append (__resource__)

from settings  import settings
from functions import *

print("*** HDMI On/Off Powersave mode starting ***")
printNote("Python version: " + str(sys.version_info))
printNote("Addon version : " + __version__)
printNote("Platform      : " + getPlatform())
printNote("UUID          : " + settings['uuid'])

# MS delay in between checking screensaver status.
WAIT_MS  = 500

platform = getPlatform()
if (not isSupportedPlatform(platform)):
	# Not the prettiest but useful to pause a bit between these notifications for UI clarity.
	xbmc.sleep(3000) 
	sendNotification("Unsupported platform: %s" % platform)
	printError("      Unsupported platform: %s" % platform)
	xbmc.sleep(3000) 
else:
	sendNotification("HDMI On/Off Powersave mode enabled")
	printNote(       "HDMI On/Off Powersave mode enabled")
	
	# Local vars
	player_stop_time       = 0
	screensaver_start_time = 0
	display_off            = False
	is_idle                = False

	# Debugging
	idle_time              = 0
	screensaver_transition = False
	
	# Check that Linux PATH environment variable contains necessary locations.
	path_to_add = ""
	if   (getPlatform() == "RaspberryPi"):
		path_to_add = "/opt/vc/bin" # for `vcgencmd`
	elif (getPlatform() == "Linux"):
		path_to_add = "/usr/bin"    # for `xset`
	if path_to_add: # Not empty string
		if path_to_add not in os.environ["PATH"].split(os.pathsep):
			os.environ["PATH"] += os.pathsep + path_to_add
	
	# -- Main Service Loop --
	while (not xbmc.abortRequested):

		powersave_seconds = settings['powersave_minutes']*60

		# Meet idle criteria after powersave_seconds seconds have elapsed following start of built-in screensaver.
		idle_time = xbmc.getGlobalIdleTime()
		is_idle = False if (time.time() - screensaver_start_time < powersave_seconds) else True
		
		# Uncomment as needed in case of wonky behavior.
		#printNote("is_idle               : %d" % is_idle)
		#printNote("powersave_minutes     : %d" % settings['powersave_minutes'])
		#printNote("powersave_seconds     : %d" % powersave_seconds)
		#printNote("idle_time             : %d" % idle_time)
		#printNote("screensaver_start_time: %d" % screensaver_start_time)
		#printNote("time_since_screensaver: %d" % (time.time() - screensaver_start_time))

		if (display_off and not is_idle):
			printDebug("turning display ON at idle time: %d" % idle_time)
			turnDisplayOn()
			display_off = False                
		
		if (xbmc.getCondVisibility("System.ScreenSaverActive")):                        
			if (not display_off and is_idle):
				printDebug("turning display OFF at idle time: %d" % idle_time)
				turnDisplayOff()
				display_off = True

			# Strictly for debugging
			if screensaver_transition:
				screensaver_transition = False
				printDebug("screensaver active at idle time: %d" % idle_time)
		else:
			# Retain the last recorded time value when screen was active.
			screensaver_transition = True
			screensaver_start_time = time.time() 
		
		# Wait for [timeout] seconds. Will stop early if abort requested.
		# Returns True when abort have been requested, False if a timeout is given and the operation times out.
		if (xbmc.Monitor().waitForAbort(float(WAIT_MS)/1000)):
			printDebug("Abort received while waiting")
			break
			
sendNotification("HDMI On/Off Powersave mode disabled")
printNote(       "HDMI On/Off Powersave mode disabled")
