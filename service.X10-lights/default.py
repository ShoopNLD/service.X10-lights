# X10-Light - Service

# IMPORT LIBRARIES
import sys
import os
import subprocess
import xbmc
import xbmcgui
import xbmcaddon
import urllib2
xbmc.log('X10-Light: ******************* X10-Light *******************')
xbmc.log('X10-Light: Import of libraries is done')
xbmc.log('X10-Light: *************************************************')

# ADDON INFORMATION
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__cwd__       = __addon__.getAddonInfo('path')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')
xbmc.log('X10-Light: *************** Addon information ***************')
xbmc.log('X10-Light: Addon info name    : ' + __addonname__)
xbmc.log('X10-Light: Addon info path    : ' + __cwd__)
xbmc.log('X10-Light: Addon info author  : ' + __author__ )
xbmc.log('X10-Light: Addon info version : ' + __version__)
xbmc.log('X10-Light: *************************************************')
xbmc.log('X10-Light: Addon information is read and shown in log file')

# ADDON HOST SETTINGS
my_ip = __addon__.getSetting("IP")
my_port = __addon__.getSetting("PORT")
# ADDON X10 DEVICE SETTINGS
my_devid = __addon__.getSetting("DEVID")
# ADDON XBMC EVENT SETTINGS
my_xevstart_tmp = __addon__.getSetting("XEVSTART")
my_xevstartperc = __addon__.getSetting("XEVSTARTPERC")
my_xevstop_tmp = __addon__.getSetting("XEVSTOP")
my_xevstopperc = __addon__.getSetting("XEVSTOPPERC")

if my_xevstart_tmp == "1":
    my_xevstart = "BRIGHT"
else:
    my_xevstart = "DIM"

if my_xevstop_tmp == "1":
    my_xevstop = "BRIGHT"
else:
    my_xevstop = "DIM"

# ADDON PLAYER EVENT SETTINGS
my_pevstart_tmp = __addon__.getSetting("PEVSTART")
my_pevstartperc = __addon__.getSetting("PEVSTARTPERC")
my_pevstop_tmp = __addon__.getSetting("PEVSTOP")
my_pevstopperc = __addon__.getSetting("PEVSTOPPERC")
my_pevpause_tmp = __addon__.getSetting("PEVPAUSE")
my_pevpauseperc = __addon__.getSetting("PEVPAUSEPERC")
my_pevresume_tmp = __addon__.getSetting("PEVRESUME")
my_pevresumeperc = __addon__.getSetting("PEVRESUMEPERC")
my_pevend_tmp = __addon__.getSetting("PEVEND")
my_pevendperc = __addon__.getSetting("PEVENDPERC")

if my_pevstart_tmp == "1":
    my_pevstart = "BRIGHT"
else:
    my_pevstart = "DIM"

if my_pevstop_tmp == "1":
    my_pevstop = "BRIGHT"
else:
    my_pevstop = "DIM"

if my_pevpause_tmp == "1":
    my_pevpause = "BRIGHT"
else:
    my_pevpause = "DIM"

if my_pevresume_tmp == "1":
    my_pevresume = "BRIGHT"
else:
    my_pevresume = "DIM"

if my_pevend_tmp == "1":
    my_pevend = "BRIGHT"
else:
    my_pevend = "DIM"

xbmc.log('X10-Light: *************** Addon Host settings *************')
xbmc.log('X10-Light: IP number          : ' + my_ip)
xbmc.log('X10-Light: PORT number        : ' + my_port)
xbmc.log('X10-Light: ************ Addon X10 Device settings **********')
xbmc.log('X10-Light: Device ID          : ' + my_devid)
xbmc.log('X10-Light: ************ Addon XBMC event settings **********')
xbmc.log('X10-Light: Start Action       : ' + my_xevstart)
xbmc.log('X10-Light: Start Action (%)   : ' + my_xevstartperc)
xbmc.log('X10-Light: Stop Action        : ' + my_xevstop)
xbmc.log('X10-Light: Stop Action (%)    : ' + my_xevstopperc)
xbmc.log('X10-Light: *********** Addon player event settings *********')
xbmc.log('X10-Light: Start Action       : ' + my_pevstart)
xbmc.log('X10-Light: Start Action (%)   : ' + my_pevstartperc)
xbmc.log('X10-Light: Stop Action        : ' + my_pevstop)
xbmc.log('X10-Light: Stop Action (%)    : ' + my_pevstopperc)
xbmc.log('X10-Light: Pause Action       : ' + my_pevpause)
xbmc.log('X10-Light: Pause Action (%)   : ' + my_pevpauseperc)
xbmc.log('X10-Light: Resume Action      : ' + my_pevresume)
xbmc.log('X10-Light: Resume Action (%)  : ' + my_pevresumeperc)
xbmc.log('X10-Light: End Action         : ' + my_pevend)
xbmc.log('X10-Light: End Action (%)     : ' + my_pevendperc)
xbmc.log('X10-Light: *************************************************')
xbmc.log('X10-Light: Addon settings are read and shown in log file')

# ADDON START
xbmc.log('X10-Light: ******************** STARTUP ********************')
#START Initialisation cycle
#Make sure Device is on
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ON"')
xbmc.log('X10-Light: Switch on Device')
#Make sure Device brightness is 100%
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' BRIGHT 100"')
xbmc.log('X10-Light: Brighten lights with 100%')
#END Initialisation cycle

xbmc.log('X10-Light: ****************** START EVENT ******************')
#Execute XBMC START Event settings on Device
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_xevstart + ' ' + my_xevstartperc + '"')
xbmc.log('X10-Light: ' + my_xevstart + 'lights with ' + my_xevstartperc + '%')
xbmc.log('X10-Light: *************************************************')

# ADDON PLAYER
xbmc.log('X10-Light: ****************** CLASS PLAYER *****************')
class MyPlayer(xbmc.Player) :
    xbmc.log('X10-Light: Class player is opened')
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        xbmc.log('X10-Light: Class player is initialized')
        
    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK STARTED')
            #Execute Player START Event settings on Device
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_pevstart + ' ' + my_pevstartperc + '"')
            xbmc.log('X10-Light: ' + my_pevstart + 'lights with ' + my_pevstartperc + '%')
            
    def onPlayBackEnded(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK ENDED')
            #Execute Player END Event settings on Device
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_pevend + ' ' + my_pevendperc + '"')
            xbmc.log('X10-Light: ' + my_pevend + 'lights with ' + my_pevendperc + '%')
            
    def onPlayBackStopped(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK STOPPED')
            #Execute Player STOP Event settings on Device
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_pevstop + ' ' + my_pevstopperc + '"')
            xbmc.log('X10-Light: ' + my_pevstop + 'lights with ' + my_pevstopperc + '%')
            
    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK PAUSED')
            #Execute Player PAUSE Event settings on Device
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_pevpause + ' ' + my_pevpauseperc + '"')
            xbmc.log('X10-Light: ' + my_pevpause + 'lights with ' + my_pevpauseperc + '%')
            
    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK RESUMED')
            #Execute Player RESUME Event settings on Device
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_pevresume + ' ' + my_pevresumeperc + '"')
            xbmc.log('X10-Light: ' + my_pevresume + 'lights with ' + my_pevresumeperc + '%')
            
player=MyPlayer()

while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0

    xbmc.sleep(1000)

while (xbmc.abortRequested):
    #Execute XBMC STOP Event settings on Device
    urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ' + my_xevstop + ' ' + my_xevstopperc + '"')
    xbmc.log('X10-Light: ' + my_xevstop + 'lights with ' + my_xevstopperc + '%')
    #MSwitch Device is off
    urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' OFF"')
    xbmc.log('X10-Light: Switch lights off')

xbmc.log('X10-Light: *************************************************')