import inspect
import xbmc
import subprocess

from settings import settings

def printDebug( msg, functionname=True ):
	if settings['debug']:
		if functionname is False:
			print(str(msg))
		else:
			print("DEBUG: HDMI Powersave - %s" % str(msg))

def printNote( msg, functionname=True ):
	if functionname is False:
		print(str(msg))
	else:
		print("NOTE: HDMI Powersave - %s" % str(msg))

def printError( msg, functionname=True ):
	if functionname is False:
		print(str(msg))
	else:
		print("ERROR: HDMI Powersave - %s" % str(msg))
		
def sendNotification(msg):
	xbmc.executebuiltin("XBMC.Notification('HDMI Powersave', '" + str(msg) + "')")
	
def getPlatform():
	# Raspberry Pi will also qualify as 'System.Platform.Linux', 
	#   so keep priority order.
	if xbmc.getCondVisibility('System.Platform.Linux.RaspberryPi'):
		return "RaspberryPi"
	elif xbmc.getCondVisibility('System.Platform.Linux'):
		return "Linux"
	elif xbmc.getCondVisibility('System.Platform.Windows'):
		return "Windows"
	elif xbmc.getCondVisibility('System.Platform.OSX'):
		return "MacOSX"
	elif xbmc.getCondVisibility('System.Platform.IOS'):
		return "iOS"
	elif xbmc.getCondVisibility('System.Platform.Darwin'):
		return "Darwin"
	elif xbmc.getCondVisibility('System.Platform.ATV2'):
		return "AppleTV2"
	elif xbmc.getCondVisibility('System.Platform.Android'): 
		return "Android"
	return "Unknown"
	
def isSupportedPlatform(platform):
	supported_platforms = ['RaspberryPi', 'Linux']
	#supported_platforms = ['RaspberryPi', 'Linux', 'Windows']
	return (platform in supported_platforms)
	
#NOTE - devshans. Could probably combine and refactor turnDisplayOff/On with a parameter
#   but keep this for now for readability and in case of bugs for a specific case.
def turnDisplayOff():
	if xbmc.getCondVisibility('System.Platform.Linux.RaspberryPi'):
		subprocess.call(["vcgencmd", "display_power", "0"])
	elif xbmc.getCondVisibility('System.Platform.Linux'):
		subprocess.call(["xset", "dpms", "force", "off"])
	elif xbmc.getCondVisibility('System.Platform.Windows'):
		try: #TODO - devshans. Windows requires external libraries or a different workaround.
			 #  May also need to fork SendMessage with a timeout
			__import__(win32gui)
			__import__(win32con)
		except ImportError:
			printError("win32* package not found.")
		else:
			SC_MONITORPOWER = 0xF170
			win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, 2)
			
def turnDisplayOn():
	if xbmc.getCondVisibility('System.Platform.Linux.RaspberryPi'):
		subprocess.call(["vcgencmd", "display_power", "1"])
	elif xbmc.getCondVisibility('System.Platform.Linux'):
		subprocess.call(["xset", "dpms", "force", "on"])
		#subprocess.call(["xset", "s", "reset"]) # May need to reset screensaver on some systems
	elif xbmc.getCondVisibility('System.Platform.Windows'):
		try: #TODO - devshans. See note in 'turnDisplayOff()'
			__import__(win32gui)
			__import__(win32con)
		except ImportError:
			printError("win32* package not found.")
		else:
			SC_MONITORPOWER = 0xF170
			win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, -1)
			