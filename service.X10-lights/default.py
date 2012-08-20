# X10-Light - Service
"""
    Document   : default.py
    Package    : X10 Commander Lights
    Author     : Majestic Soft
    Copyright  : 2012, Majestic Soft, NL
    License    : Gnu General Public License - see LICENSE.TXT
    Description: General control code for X10 Commander Lights
    Revision   : 0.0.6 beta
                 Added: Thinking Home (via webserver support)
    Revision   : 0.0.6 alpha
                 Added: Enable/Disable of Events
                 Added: Free or predefinded commands per Event
                 Added: Switch King
                 Added: Username/password option
                 Updated: [CORE] Selection function to handle Free commands
                 Updated: [CORE] Application functions to handle Free commands
                 Updated: [CORE] Multiple Device's (to maximum of five device's)
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
def X10Commander(URL, ID, Action, Value, FreeCmd):
    #X10-COMMANDER STYLE
    #Example strings
    #In which: my_url = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"
    #urllib2.urlopen(my_url + DeviceID + ' ON"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 ON"
    #urllib2.urlopen(my_url + DeviceID + ' OFF"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 OFF"
    #urllib2.urlopen(my_url + DeviceID + ' BRIGHT ' + DevicePercentage + '"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 BRIGHT 50"
    #urllib2.urlopen(my_url + DeviceID + ' DIM ' + DevicePercentage + '"') = http://172.0.0.1:8086/?x10command=DEVICE~sendplc~"A1 BRIGHT 100"
    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
        if FreeCmd:
            ActionData = ID + ' ' + Action + ' '+ Value + '"'
            xbmc.log('X10-Light: X10-Commander, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + ' ON"'
                xbmc.log('X10-Light: X10-Commander, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + ' OFF"'
                xbmc.log('X10-Light: X10-Commander, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + ' BRIGHT ' + Value + '"'
                xbmc.log('X10-Light: X10-Commander, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + ' DIM ' + Value + '"'
                xbmc.log('X10-Light: X10-Commander, Dim lights with ' + Value + '%')
            else:
                xbmc.log('X10-Light: X10-Commander, No Action available!')

        xbmc.log('X10-Light: X10-Commander, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to X10-Commander')
    except:
        xbmc.log('X10-Light: X10-Commander, The ' + Action + ' Event Failed')
    return

# HOMESEER FUNCTION 
#This function Will execute the requested action in HomeSeer 
def HomeSeer(URL, ID, Action, Value, FreeCmd):
    #HOMESEER STYLE
    #Example strings
    #urllib2.urlopen(my_url, my_data), this is with a comma, since the my_data needs to be encoded
    try:
        if FreeCmd:
            ActionData = urllib.urlencode({'control_device':ID + '=' + Action + '=' + Value})
            xbmc.log('X10-Light: HomeSeer, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = urllib.urlencode({'control_device':ID + '=ON'})
                xbmc.log('X10-Light: HomeSeer, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = urllib.urlencode({'control_device':ID + '=OFF'})
                xbmc.log('X10-Light: HomeSeer, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = urllib.urlencode({'control_device':ID + '=BRIGHT=' + Value})
                xbmc.log('X10-Light: HomeSeer, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = urllib.urlencode({'control_device':ID + '=DIM=' + Value})
                xbmc.log('X10-Light: HomeSeer, Dim lights with ' + Value + '%')
            else:
                xbmc.log('X10-Light: HomeSeer, No Action available!')

        HomeSeerRequest = urllib2.urlopen(URL, ActionData)
        xbmc.log('X10-Light: HomeSeer, Request: ' + HomeSeerRequest)
        xbmc.log('X10-Light: Action Send to HomeSeer')
    except:
        xbmc.log('X10-Light: HomeSeer, XBMC ' + Action + ' Event Failed')
    return

# TENHSSERVER FUNCTION 
#This function Will execute the requested action in HomeSeer via tenHsServer
def tenHsServer(URL, ID, Action, Value, FreeCmd):
    #tenHsServer STYLE
    #Example strings
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=ON')
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=BRIGHT&s=100')
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=' + my_xevstart + '&s=' + my_xevstartperc + '')
    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
        if FreeCmd:
            ActionData = ID + '&a=' + Action + '&s=' + Value + ''
            xbmc.log('X10-Light: tenHsServer, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '&a=ON'
                xbmc.log('X10-Light: tenHsServer, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '&a=OFF'
                xbmc.log('X10-Light: tenHsServer, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '&a=BRIGHT&s=' + Value + ''
                xbmc.log('X10-Light: tenHsServer, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '&a=DIM&s=' + Value + ''
                xbmc.log('X10-Light: tenHsServer, Dim lights with ' + Value + '%')
            else:
                xbmc.log('X10-Light: tenHsServer, No Action available!')

        xbmc.log('X10-Light: tenHsServer, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to tenHsServer')
    except:
        xbmc.log('X10-Light: tenHsServer, The ' + Action + ' Event Failed')
    return

# SWITCH KING FUNCTION 
#This function Will execute the requested action in Switch king
def SwitchKing(URL, ID, Action, Value, FreeCmd):
    #Switch King STYLE
    #Example strings
    #http://servernamn:8800/devices/{id}/turnon
    #http://servernamn:8800/devices/{id}/turnoff
    #http://servernamn:8800/devices/{id}/dim/{level}
    try:
        if FreeCmd:
            ActionData = ID + '/' + Action + '/' + Value
            xbmc.log('X10-Light: Switch King, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '/turnon'
                xbmc.log('X10-Light: Switch King, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '/turnoff'
                xbmc.log('X10-Light: Switch King, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '/bright/' + Value + ''
                xbmc.log('X10-Light: Switch King, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '/dim/' + Value + ''
                xbmc.log('X10-Light: Switch King, Dim lights with ' + Value + '%')
            else:
                xbmc.log('X10-Light: Switch King, No Action available!')

        xbmc.log('X10-Light: Switch King, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to Switch King')
    except:
        xbmc.log('X10-Light: Switch King, The ' + Action + ' Event Failed')
    return

# THINKING HOME FUNCTION 
#This function Will execute the requested action in Thinking Home
def ThinkingHome(URL, ID, Action, Value, FreeCmd):
    #ThinkingHome STYLE
    #Example strings
    #http://servername:port/cgi-bin/thinkingHome-cgi?devName={id}&action=turnon
    #http://servername:port/cgi-bin/thinkingHome-cgi?devName={id}&action=turnoff
    #http://servername:port/cgi-bin/thinkingHome-cgi?devName={id}&action=dim&amount={value}
    #http://servername:port/cgi-bin/thinkingHome-cgi?devName={id}&action=bright&amount={value}

    try:
        if FreeCmd:
            ActionData = ID + '&action=' + Action + '&amount=' + Value
            xbmc.log('X10-Light: Thinking Home, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '&action=turnon'
                xbmc.log('X10-Light: Thinking Home, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '&action=turnoff'
                xbmc.log('X10-Light: Thinking Home, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '&action=bright&amount=' + Value
                xbmc.log('X10-Light: Thinking Home, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '&action=dim&amount=' + Value
                xbmc.log('X10-Light: Thinking Home, Dim lights with ' + Value + '%')
            else:
                xbmc.log('X10-Light: Thinking Home, No Action available!')

        xbmc.log('X10-Light: Thinking Home, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        xbmc.log('X10-Light: Action Send to Thinking Home')
    except:
        xbmc.log('X10-Light: Thinking Home, The ' + Action + ' Event Failed')
    return

# EXECUTEACTION FUNCTION
def ExecuteAction(Application, URL, ID, Action, Value, FreeCmd):
    #This function is a simple selector 
    #It will call the correct Application to execute the desired action
    #This section should be expended with new aplication as they come available
    if Application == "X10-COMMANDER":
        X10Commander(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMESEER":
        HomeSeer(URL, ID, Action, Value, FreeCmd)
    elif Application == "TENHSSERVER":
        tenHsServer(URL, ID, Action, Value, FreeCmd)
    elif Application == "SWITCHKING":
        SwitchKing(URL, ID, Action, Value, FreeCmd)
    elif Application == "THINKINGHOME":
        ThinkingHome(URL, ID, Action, Value, FreeCmd)
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
# User:Pass@

if __addon__.getSetting("DEVAPP") == "0":
    DeviceApplication = "X10-COMMANDER"
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("USER") + ':' + __addon__.getSetting("PASS") + '@' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/?x10command=DEVICE~sendplc~"'
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/?x10command=DEVICE~sendplc~"'
elif __addon__.getSetting("DEVAPP") == "1":
    #Security unkown
    DeviceApplication = "HOMESEER"
    DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/tail.htm'
elif __addon__.getSetting("DEVAPP") == "2":
    DeviceApplication = "TENHSSERVER"
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("USER") + ':' + __addon__.getSetting("PASS") + '@' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d='
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d='
elif __addon__.getSetting("DEVAPP") == "3":
    DeviceApplication = "SWITCHKING"
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("USER") + ':' + __addon__.getSetting("PASS") + '@' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/devices/'
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/devices/'
elif __addon__.getSetting("DEVAPP") == "4":
    DeviceApplication = "THINKINGHOME"
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("USER") + ':' + __addon__.getSetting("PASS") + '@' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/cgi-bin/thinkingHome-cgi?devName='
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/cgi-bin/thinkingHome-cgi?devName='
else:
    DeviceApplication = "UNKOWN"

xbmc.log('X10-Light: Security: ' + str(__addon__.getSetting("SECURITY")))
xbmc.log('X10-Light: Base URL: ' + DeviceURL)

# ADDON DEVICE SETTINGS
DeviceID = __addon__.getSetting("DEVID01")

# ADDON EVENT SETTINGS
# ADDON XBMC AND PLAYER EVENT SETTINGS (depening on Free definable Action command's = 1 or Fixed Action command's = 0)
# with Free definable Action command's, the user has to type his own commands, and if needed his own value's
# with Fixed Action command's, the user has can select the appropriate action (ON/OFF/DIM/BRIGHT), and if need fill out a percentage.
#XBMC
xbmc.log('X10-Light: StartEventEnable: ' + __addon__.getSetting("XEVSTARTENABLE01"))
xbmc.log('X10-Light: StartFree: ' + __addon__.getSetting("XEVSTARTFREE01"))
XBMCStartEventEnable = __addon__.getSetting("XEVSTARTENABLE01")
XBMCStartFreeCmd = __addon__.getSetting("XEVSTARTFREE01")
if __addon__.getSetting("XEVSTARTFREE01"):
    XBMCStartEvent = __addon__.getSetting("XEVSTARTCMD01")
    XBMCStartValue = __addon__.getSetting("XEVSTARTVAL01")
else:
    XBMCStartEvent = EventAction(__addon__.getSetting("XEVSTART01"))
    XBMCStartValue = __addon__.getSetting("XEVSTARTPERC01")

XBMCStopEventEnable = __addon__.getSetting("XEVSTOPENABLE01")
XBMCStopFreeCmd = __addon__.getSetting("XEVSTOPFREE01")
if __addon__.getSetting("XEVSTOPFREE01"):
    XBMCStopEvent = __addon__.getSetting("XEVSTOPCMD01")
    XBMCStopValue = __addon__.getSetting("XEVSTOPVAL01")
else:
    XBMCStopEvent = EventAction(__addon__.getSetting("XEVSTOP01"))
    XBMCStopValue = __addon__.getSetting("XEVSTOPPERC01")

#PLAYER
PLAYERStartEventEnable = __addon__.getSetting("PEVSTARTENABLE01")
PLAYERStartFreeCmd = __addon__.getSetting("PEVSTARTFREE01")
if __addon__.getSetting("PEVSTARTFREE01"):
    PLAYERStartEvent = __addon__.getSetting("PEVSTARTCMD01")
    PLAYERStartValue = __addon__.getSetting("PEVSTARTVAL01")
else:
    PLAYERStartEvent = EventAction(__addon__.getSetting("PEVSTART01"))
    PLAYERStartValue = __addon__.getSetting("PEVSTARTPERC01")

PLAYERStopEventEnable = __addon__.getSetting("PEVSTOPENABLE01")
PLAYERStopFreeCmd = __addon__.getSetting("PEVSTOPFREE01")
if __addon__.getSetting("PEVSTOPFREE01"): 
    PLAYERStopEvent = __addon__.getSetting("PEVSTOPCMD01")
    PLAYERStopValue = __addon__.getSetting("PEVSTOPVAL01")
else:
    PLAYERStopEvent = EventAction(__addon__.getSetting("PEVSTOP01"))
    PLAYERStopValue = __addon__.getSetting("PEVSTOPPERC01")

PLAYERPauseEventEnable = __addon__.getSetting("PEVPAUSEENABLE01")
PLAYERPauseFreeCmd = __addon__.getSetting("PEVPAUSEFREE01")
if __addon__.getSetting("PEVPAUSEFREE01"): 
    PLAYERPauseEvent = __addon__.getSetting("PEVPAUSECMD01")
    PLAYERPauseValue = __addon__.getSetting("PEVPAUSEVAL01")
else:
    PLAYERPauseEvent = EventAction(__addon__.getSetting("PEVPAUSE01"))
    PLAYERPauseValue = __addon__.getSetting("PEVPAUSEPERC01")

PLAYERResumeEventEnable = __addon__.getSetting("PEVRESUMEENABLE01")
PLAYERResumeFreeCmd = __addon__.getSetting("PEVPAUSEFREE01")
if __addon__.getSetting("PEVPAUSEFREE01"): 
    PLAYERResumeEvent = __addon__.getSetting("PEVRESUMECMD01")
    PLAYERResumeValue = __addon__.getSetting("PEVRESUMEVAL01")
else:
    PLAYERResumeEvent = EventAction(__addon__.getSetting("PEVRESUME01"))
    PLAYERResumeValue = __addon__.getSetting("PEVRESUMEPERC01")

PLAYEREndEventEnable = __addon__.getSetting("PEVENDENABLE01")
PLAYEREndFreeCmd = __addon__.getSetting("PEVPAUSEFREE01")
if __addon__.getSetting("PEVPAUSEFREE01"): 
    PLAYEREndEvent = __addon__.getSetting("PEVENDCMD01")
    PLAYEREndValue = __addon__.getSetting("PEVENDVAL01")
else:
    PLAYEREndEvent = EventAction(__addon__.getSetting("PEVEND01"))
    PLAYEREndValue = __addon__.getSetting("PEVENDPERC01")

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
    xbmc.log('X10-Light: Start Action (%)   : ' + XBMCStartValue)
xbmc.log('X10-Light: Stop Action        : ' + XBMCStopEvent)
if XBMCStopEvent == "BRIGHT" or XBMCStopEvent == "DIM":
    xbmc.log('X10-Light: Stop Action (%)    : ' + XBMCStopValue)
xbmc.log('X10-Light: *********** Addon player event settings *********')
xbmc.log('X10-Light: Start Action       : ' + PLAYERStartEvent)
if PLAYERStartEvent == "BRIGHT" or PLAYERStartEvent == "DIM":
    xbmc.log('X10-Light: Start Action (%)   : ' + PLAYERStartValue)
xbmc.log('X10-Light: Stop Action        : ' + PLAYERStopEvent)
if PLAYERStopEvent == "BRIGHT" or PLAYERStopEvent == "DIM":
    xbmc.log('X10-Light: Stop Action (%)    : ' + PLAYERStopValue)
xbmc.log('X10-Light: Pause Action       : ' + PLAYERPauseEvent)
if PLAYERPauseEvent == "BRIGHT" or PLAYERPauseEvent == "DIM":
    xbmc.log('X10-Light: Pause Action (%)   : ' + PLAYERPauseValue)
xbmc.log('X10-Light: Resume Action      : ' + PLAYERResumeEvent)
if PLAYERResumeEvent == "BRIGHT" or PLAYERResumeEvent == "DIM":
    xbmc.log('X10-Light: Resume Action (%)  : ' + PLAYERResumeValue)
xbmc.log('X10-Light: End Action         : ' + PLAYEREndEvent)
if PLAYEREndEvent == "BRIGHT" or PLAYEREndEvent == "DIM":
    xbmc.log('X10-Light: End Action (%)     : ' + PLAYEREndValue)
xbmc.log('X10-Light: *************************************************')
xbmc.log('X10-Light: Addon settings are read and shown in log file')

# ADDON START
xbmc.log('X10-Light: ******************** STARTUP ********************')

#START Initialisation cycle
xbmc.log('X10-Light: **************** INITIALIZATION******************')
#Make sure Device is on
ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "ON", "0", "false")
#Make sure Device brightness is 100%
ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "BRIGHT", "100", "false")
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
if XBMCStartEventEnable=="true":
    ExecuteAction(DeviceApplication, DeviceURL, DeviceID, XBMCStartEvent, XBMCStartValue, XBMCStartFreeCmd)
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
            if PLAYERStartEventEnable=="true":
                xbmc.log('X10-Light: PLAYBACK STARTED')
                ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERStartEvent, PLAYERStartValue, PLAYERStartFreeCmd)

    def onPlayBackEnded(self):
        if (VIDEO == 1):
            if PLAYEREndEventEnable=="true":
                xbmc.log('X10-Light: PLAYBACK ENDED')
                #Execute Player END Event settings on Device
                ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYEREndEvent, PLAYEREndValue, PLAYEREndFreeCmd)

    def onPlayBackStopped(self):
        if (VIDEO == 1):
            if PLAYERStopEventEnable=="true":
                xbmc.log('X10-Light: PLAYBACK STOPPED')
                #Execute Player STOP Event settings on Device
                ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERStopEvent, PLAYERStopValue, PLAYERStopFreeCmd)
 
    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            if PLAYERPausedEventEnable=="true":
                xbmc.log('X10-Light: PLAYBACK PAUSED')
                #Execute Player PAUSE Event settings on Device
                ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERPauseEvent, PLAYERPauseValue, PLAYERPauseFreeCmd)

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            if PLAYERResumeEventEnable=="true":
                xbmc.log('X10-Light: PLAYBACK RESUMED')
                #Execute Player RESUME Event settings on Device
                ExecuteAction(DeviceApplication, DeviceURL, DeviceID, PLAYERResumeEvent, PLAYERResumeValue, PLAYERResumeFreeCmd)

player=MyPlayer()

while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0

    xbmc.sleep(1000)

if (xbmc.abortRequested):
    if XBMCStopEventEnable=="true":
        #START XBMC STOP Event
        xbmc.log('X10-Light: ****************** STOP EVENT ******************')
        ExecuteAction(DeviceApplication, DeviceURL, DeviceID, XBMCStopEvent, XBMCStopValue, XBMCStopFreeCmd)
        xbmc.log('X10-Light: *************************************************')
        #END XBMC STOP Event
        #Execute XBMC STOP Event settings on Device

    if XBMCStopEventEnable=="true":
        #MSwitch Device is off
        ExecuteAction(DeviceApplication, DeviceURL, DeviceID, "OFF", "0", "false")

xbmc.log('X10-Light: *************************************************')