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

# ADDON SETTINGS
my_ip = __addon__.getSetting("IP")
my_port = __addon__.getSetting("PORT")
my_devid = __addon__.getSetting("DEVID")
xbmc.log('X10-Light: ***************** Addon settings ****************')
xbmc.log('X10-Light: IP number          : ' + my_ip)
xbmc.log('X10-Light: PORT number        : ' + my_port)
xbmc.log('X10-Light: Device ID          : ' + my_devid)
xbmc.log('X10-Light: *************************************************')
xbmc.log('X10-Light: Addon settings are read and shown in log file')

# ADDON STARTUP
xbmc.log('X10-Light: ******************** STARTUP ********************')
#Example layout of a url call to X10 Commander
#urllib2.urlopen('http://192.168.1.1:8086/?x10command=DEVICE~sendplc~"A1 BRIGHT 100"')
#Make sure Device is on
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' ON"')
xbmc.log('X10-Light: Switch on Device')
#Make sure Device brightness is 100%
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' BRIGHT 100"')
xbmc.log('X10-Light: Brighten lights with 100%')
#Dim Device to 50%
urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' DIM 50"')
xbmc.log('X10-Light: Brighten DIM with 50%')
xbmc.log('X10-Light: *************************************************')

# ADDON TODO
xbmc.log('X10-Light: ****************** CLASS PLAYER *****************')
class MyPlayer(xbmc.Player) :
    xbmc.log('X10-Light: Class player is opened')
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        xbmc.log('X10-Light: Class player is initialized')
        
    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK STARTED')
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' DIM 100"')
            xbmc.log('X10-Light: Dim lights with 100%')
            
    def onPlayBackEnded(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK ENDED')
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' BRIGHT 50"')
            xbmc.log('X10-Light: Brighten lights with 50%')
            
    def onPlayBackStopped(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK STOPPED')
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' BRIGHT 50"')
            xbmc.log('X10-Light: Brighten lights with 50%')
            
    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK PAUSED')
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' BRIGHT 50"')
            xbmc.log('X10-Light: Brighten lights with 50%')
            
    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK RESUMED')
            urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' DIM 100"')
            xbmc.log('X10-Light: Dim lights with 100%')
            
player=MyPlayer()

#while(1):
while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0
        
    xbmc.sleep(3000)
    
while (xbmc.abortRequested):
    #Dim Device with 100%
    urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' DIM 100"')
    xbmc.log('X10-Light: Dim lights with 100%')
    #MSwitch Device is off
    urllib2.urlopen('http://' + my_ip + ':' + my_port + '/?x10command=DEVICE~sendplc~"' + my_devid + ' OFF"')
    xbmc.log('X10-Light: Switch lights off')

xbmc.log('X10-Light: *************************************************')