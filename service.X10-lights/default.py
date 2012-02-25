# X10-Light - Service
"""
    Document   : default.py
    Package    : X10 Commander Lights
    Author     : Majestic Soft
    Copyright  : 2011, Majestic Soft, NL
    License    : Gnu General Public License - see LICENSE.TXT
    Description: General control code for X10 Commander Lights
    Revision   : 0.0.5
                 Solved: Issue 1, No more error message at startup when Add-on is not configured (Clean install)
                 Solved: Issue 2, Stop event is now working.
                 Changed: [CORE] X10-Commander handling to seperate function (for easier expansion of new Applications)
                 Changed: [CORE] HomeSeer handling to seperate function (for easier expansion of new Applications)
                 Added: [CORE] Selection function to call the appropriate Application function.
                 Added: Improved fault handling and logging on event failure's
                 Added: Device Actions (ON and OFF) to events
                 Added: tenHsServer to see how easy modularity now works.
    Revision   : 0.0.4
                 Updated: HomeSeer control (removed tenHsServer)
    Revision   : 0.0.3
                 Added: this descriptive text
                 Added: HomeSeer control via tenHsServer (http://www.tenholder.net/tenWare2/tenHsServer/default.aspx)
"""
# IMPORT LIBRARIES
import sys
import os
import subprocess
import xbmc
import xbmcgui
import xbmcaddon
import urllib
import urllib2

# FUNCTIONS - START

# X10-COMMANDER FUNCTION
#This function Will execute the requested action in X10-Commander 
def X10Commander(URL, ID, Action, Percentage):
    #X10-COMMANDER STYLE
    #Example strings
    #In which: my_url = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"
    #urllib2.urlopen(my_url + DeviceID + ' ON"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 ON"
    #urllib2.urlopen(my_url + DeviceID + ' OFF"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 OFF"
    #urllib2.urlopen(my_url + DeviceID + ' BRIGHT ' + DevicePercentage + '"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 BRIGHT 50"
    #urllib2.urlopen(my_url + DeviceID + ' DIM ' + DevicePercentage + '"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 BRIGHT 100"
    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
        if Action == "ON":
            ActionData = ID + ' ON"'
            xbmc.log('X10-Light: Switch lights or Device ON')
        elif Action == "OFF":
            ActionData = ID + ' OFF"'
            xbmc.log('X10-Light: Switch lights or Device OFF')
        elif Action == "BRIGHT":
            ActionData = ID + ' BRIGHT ' + Percentage + '"'
            xbmc.log('X10-Light: Brighten lights with ' + Percentage + '%')
        elif Action == "DIM":
            ActionData = ID + ' DIM ' + Percentage + '"'
            xbmc.log('X10-Light: Dim lights with ' + Percentage + '%')
        else:
            xbmc.log('X10-Light: No Action available!')

        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to X10-Commander')
    except:
        xbmc.log('X10-Light: The ' + Action + ' Event Failed')
    return

# HOMESEER FUNCTION 
#This function Will execute the requested action in HomeSeer 
def HomeSeer(URL, ID, Action, Percentage):
    #HOMESEER STYLE
    #Example strings
    #urllib2.urlopen(my_url, my_data), this is with a comma, since the my_data needs to be encoded
    try:
        if Action == "ON":
            ActionData = urllib.urlencode({'control_device':ID + '=ON'})
            xbmc.log('X10-Light: Switch lights or Device ON')
        elif Action == "OFF":
            ActionData = urllib.urlencode({'control_device':ID + '=OFF'})
            xbmc.log('X10-Light: Switch lights or Device OFF')
        elif Action == "BRIGHT":
            ActionData = urllib.urlencode({'control_device':ID + '=BRIGHT=' + Percentage})
            xbmc.log('X10-Light: Brighten lights with ' + Percentage + '%')
        elif Action == "DIM":
            ActionData = urllib.urlencode({'control_device':ID + '=DIM=' + Percentage})
            xbmc.log('X10-Light: Dim lights with ' + Percentage + '%')
        else:
            xbmc.log('X10-Light: No Action available!')

        HomeSeerRequest = urllib2.urlopen(URL, ActionData)
        xbmc.log('X10-Light: Action Send to HomeSeer')
    except:
        xbmc.log('X10-Light: XBMC ' + Action + ' Event Failed')
    return

# TENHSSERVER FUNCTION 
#This function Will execute the requested action in HomeSeer via tenHsServer
def tenHsServer(URL, ID, Action, Percentage):
    #tenHsServer STYLE
    #Example strings
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=ON')
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=BRIGHT&s=100')
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=' + my_xevstart + '&s=' + my_xevstartperc + '')
    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
        if Action == "ON":
            ActionData = ID + '&a=ON'
            xbmc.log('X10-Light: Switch lights or Device ON')
        elif Action == "OFF":
            ActionData = ID + '&a=OFF'
            xbmc.log('X10-Light: Switch lights or Device OFF')
        elif Action == "BRIGHT":
            ActionData = ID + '&a=BRIGHT&s=' + Percentage + ''
            xbmc.log('X10-Light: Brighten lights with ' + Percentage + '%')
        elif Action == "DIM":
            ActionData = ID + '&a=DIM&s=' + Percentage + ''
            xbmc.log('X10-Light: Dim lights with ' + Percentage + '%')
        else:
            xbmc.log('X10-Light: No Action available!')

        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to tenHsServer')
    except:
        xbmc.log('X10-Light: The ' + Action + ' Event Failed')
    return

# EXECUTEACTION FUNCTION
def ExecuteAction(Application, URL, ID, Action, Percentage):
    #This function is a simple selector 
    #It will call the correct Application to execute the desired action
    #This section should be expended with new aplication as they come available
    if Application == "X10-COMMANDER":
        X10Commander(URL, ID, Action, Percentage)
    elif Application == "HOMESEER":
        HomeSeer(URL, ID, Action, Percentage)
    elif Application == "TENHSSERVER":
        tenHsServer(URL, ID, Action, Percentage)
    else:
        xbmc.log('X10-Light: An unknown Device Aplication is selected!')
    return

# EVENTACTION FUNCTION
def EventAction(Action):
    #This function is a simple selector that returns the action as a text to the event
    #(it simply converst a number to string)
    if Action == "3":
        ReturnValue = "OFF"
    elif Action == "2":
        ReturnValue = "ON"
    elif Action == "1":
        ReturnValue = "BRIGHT"
    else:
        ReturnValue = "DIM"
    return ReturnValue

# FUNCTIONS - END

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

# ADDON DEVICE APPLICATION AND URL SETTING
# 'http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=ON'

if __addon__.getSetting("DEVAPP") == "0":
    DeviceApplication = "X10-COMMANDER"
    DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/?x10command=DEVICE~sendplc~"'
elif __addon__.getSetting("DEVAPP") == "1":
    DeviceApplication = "HOMESEER"
    DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/tail.htm'
elif __addon__.getSetting("DEVAPP") == "2":
    DeviceApplication = "TENHSSERVER"
    DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d='
else:
    DeviceApplication = "UNKOWN"

# ADDON DEVICE SETTINGS
DeviceID = __addon__.getSetting("DEVID")

# ADDON XBMC EVENT SETTINGS
XBMCStartEvent = EventAction(__addon__.getSetting("XEVSTART"))
XBMCStartPercentage = __addon__.getSetting("XEVSTARTPERC")
XBMCStopEvent = EventAction(__addon__.getSetting("XEVSTOP"))
XBMCStopPercentage = __addon__.getSetting("XEVSTOPPERC")

# ADDON PLAYER EVENT SETTINGS
PLAYERStartEvent = EventAction(__addon__.getSetting("PEVSTART"))
PLAYERStartPercentage = __addon__.getSetting("PEVSTARTPERC")
PLAYERStopEvent = EventAction(__addon__.getSetting("PEVSTOP"))
PLAYERStopPercentage = __addon__.getSetting("PEVSTOPPERC")
PLAYERPauseEvent = EventAction(__addon__.getSetting("PEVPAUSE"))
PLAYERPausePercentage = __addon__.getSetting("PEVPAUSEPERC")
PLAYERResumeEvent = EventAction(__addon__.getSetting("PEVRESUME"))
PLAYERResumePercentage = __addon__.getSetting("PEVRESUMEPERC")
PLAYEREndEvent = EventAction(__addon__.getSetting("PEVEND"))
PLAYEREndPercentage = __addon__.getSetting("PEVENDPERC")

# ADDON SHOW INFORMATION ABOUT ALL SETTINGS
xbmc.log('X10-Light: *************** Addon Host settings *************')
xbmc.log('X10-Light: IP number          : ' + str(__addon__.getSetting("IP")))
xbmc.log('X10-Light: PORT number        : ' + str(__addon__.getSetting("PORT")))
xbmc.log('X10-Light: ************ Addon X10 Device settings **********')
xbmc.log('X10-Light: Device ID          : ' + DeviceID)
xbmc.log('X10-Light: Device Application : ' + DeviceApplication)
xbmc.log('X10-Light: ************ Addon XBMC event settings **********')
xbmc.log('X10-Light: Start Action       : ' + XBMCStartEvent)
if XBMCStartEvent == "BRIGHT" or XBMCStartEvent == "DIM":
    xbmc.log('X10-Light: Start Action (%)   : ' + XBMCStartPercentage)
xbmc.log('X10-Light: Stop Action        : ' + XBMCStopEvent)
if XBMCStopEvent == "BRIGHT" or XBMCStopEvent == "DIM":
    xbmc.log('X10-Light: Stop Action (%)    : ' + XBMCStopPercentage)
xbmc.log('X10-Light: *********** Addon player event settings *********')
xbmc.log('X10-Light: Start Action       : ' + PLAYERStartEvent)
if PLAYERStartEvent == "BRIGHT" or PLAYERStartEvent == "DIM":
    xbmc.log('X10-Light: Start Action (%)   : ' + PLAYERStartPercentage)
xbmc.log('X10-Light: Stop Action        : ' + PLAYERStopEvent)
if PLAYERStopEvent == "BRIGHT" or PLAYERStopEvent == "DIM":
    xbmc.log('X10-Light: Stop Action (%)    : ' + PLAYERStopPercentage)
xbmc.log('X10-Light: Pause Action       : ' + PLAYERPauseEvent)
if PLAYERPauseEvent == "BRIGHT" or PLAYERPauseEvent == "DIM":
    xbmc.log('X10-Light: Pause Action (%)   : ' + PLAYERPausePercentage)
xbmc.log('X10-Light: Resume Action      : ' + PLAYERResumeEvent)
if PLAYERResumeEvent == "BRIGHT" or PLAYERResumeEvent == "DIM":
    xbmc.log('X10-Light: Resume Action (%)  : ' + PLAYERResumePercentage)
xbmc.log('X10-Light: End Action         : ' + PLAYEREndEvent)
if PLAYEREndEvent == "BRIGHT" or PLAYEREndEvent == "DIM":
    xbmc.log('X10-Light: End Action (%)     : ' + PLAYEREndPercentage)
xbmc.log('X10-Light: *************************************************')
xbmc.log('X10-Light: Addon settings are read and shown in log file')

# ADDON START
xbmc.log('X10-Light: ******************** STARTUP ********************')

#START Initialisation cycle
xbmc.log('X10-Light: **************** INITIALIZATION******************')
#Make sure Device is on
ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "ON", "0")
#Make sure Device brightness is 100%
ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "BRIGHT", "100")
xbmc.log('X10-Light: *************************************************')
#END Initialisation cycle

#START XBMC START Event
xbmc.log('X10-Light: ****************** START EVENT ******************')
#REMARK (explanation to the call):
#Application, URL, are always the same.
#Since only one device can be connected to the Add-on, this is also valid for the ID
#The ID is prepeared so in later versions it is possible to us the function call on different Device's
#Determine Action and Percentage (this depends only on the appropriate settings)

#CALL Function, to ececute the action
ExecuteAction(DeviceApplication, DeviceURL, DeviceID, XBMCStartEvent, XBMCStartPercentage)
xbmc.log('X10-Light: *************************************************')
#END XBMC START Event

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
            ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERStartEvent, PLAYERStartPercentage)

    def onPlayBackEnded(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK ENDED')
            #Execute Player END Event settings on Device
            ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYEREndEvent, PLAYEREndPercentage)

    def onPlayBackStopped(self):
        if (VIDEO == 1):
            xbmc.log('X10-Light: PLAYBACK STOPPED')
            #Execute Player STOP Event settings on Device
            ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERStopEvent, PLAYERStopPercentage)
 
    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK PAUSED')
            #Execute Player PAUSE Event settings on Device
            ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERPauseEvent, PLAYERPausePercentage)

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            xbmc.log('X10-Light: PLAYBACK RESUMED')
            #Execute Player RESUME Event settings on Device
            ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERResumeEvent, PLAYERResumePercentage)

player=MyPlayer()

while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0

    xbmc.sleep(1000)

if (xbmc.abortRequested):
    #START XBMC STOP Event
    xbmc.log('X10-Light: ****************** STOP EVENT ******************')
    ExecuteAction(DeviceApplication, DeviceURL, DeviceID, XBMCStopEvent, XBMCStopPercentage)
    xbmc.log('X10-Light: *************************************************')
    #END XBMC STOP Event
    #Execute XBMC STOP Event settings on Device
    
    #MSwitch Device is off
    ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "OFF", "0")

xbmc.log('X10-Light: *************************************************')