# X10 - Lights (Domotica Commander) - Service
"""
    Document   : default.py
    Package    : X10 - Lights (Domotica Commander)
    Author     : Majestic Soft
    Copyright  : 2013, Majestic Soft, NL
    License    : Gnu General Public License - see LICENSE.TXT
    Description: General control code for X10 - Lights (Domotica Commander)
    Revision   : 1.0.1 
                 Added: Domoticz.
                 Fixed: bug in HomeWizard call.
                 Updated: zip file structure to support the import from zip file option in xbmc
                 Updated: The Manual
    Revision   : 1.0.0 
                 Added: Thinking Home (via webserver support)
                 Added: HomeWizard
                 Added: Enable/Disable of Debugging text
                 Changed: Name from X10 Commander Lights to X10 - Lights (Domotica Commander)
                 Updated: [CORE] Multiple Device's (to maximum of five device's)
                 Updated: [CORE] Improved Event Handling (easy support of multiple device's)
                 Updated: [CORE] Default Initialization actions (for Start and Stop) removed
                 Updated: Some text strins in the configuration
                 Updated: The Manual
    Revision   : 0.0.6 alpha
                 Added: Enable/Disable of Events
                 Added: Free or predefinded commands per Event
                 Added: Switch King
                 Added: Username/password option
                 Updated: [CORE] Selection function to handle Free commands
                 Updated: [CORE] Application functions to handle Free commands
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

#Initialize ADDON
__addon__     = xbmcaddon.Addon()

#Initialize ADDON LOG Settings (for Debugging)
xbmc.log('X10-Lights: ******************* X10-Lights ******************')
if (str(__addon__.getSetting("DEBUGLOG")) == "true"):
    debuging = True
    xbmc.log('X10-Lights: Debuging log files is on')
else:
    debuging = False
    xbmc.log('X10-Lights: Debuging log files is off')
    xbmc.log('X10-Lights: *************************************************')

#Initialize ADDON INFORMATION
__addonname__ = __addon__.getAddonInfo('name')
__cwd__       = __addon__.getAddonInfo('path')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')

if (debuging): 
    xbmc.log('X10-Lights: *************** Addon information ***************')
    xbmc.log('X10-Lights: Addon info name    : ' + __addonname__)
    xbmc.log('X10-Lights: Addon info path    : ' + __cwd__)
    xbmc.log('X10-Lights: Addon info author  : ' + __author__ )
    xbmc.log('X10-Lights: Addon info version : ' + __version__)
    xbmc.log('X10-Lights: *************************************************')

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
            if (debuging): xbmc.log('X10-Lights: X10-Commander, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + ' ON"'
                if (debuging): xbmc.log('X10-Lights: X10-Commander, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + ' OFF"'
                if (debuging): xbmc.log('X10-Lights: X10-Commander, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + ' BRIGHT ' + Value + '"'
                if (debuging): xbmc.log('X10-Lights: X10-Commander, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + ' DIM ' + Value + '"'
                if (debuging): xbmc.log('X10-Lights: X10-Commander, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: X10-Commander, No Action available!')

        if (debuging): xbmc.log('X10-Lights: X10-Commander, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to X10-Commander')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: X10-Commander, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

# HOMESEER FUNCTION 
#This function Will execute the requested action in HomeSeer 
def HomeSeer(URL, ID, Action, Value, FreeCmd):
    #HOMESEER STYLE
    #Example strings
    #urllib2.urlopen(my_url, my_data), this is with a comma, since the my_data needs to be encoded
    try:
        if FreeCmd:
            ActionData = urllib.urlencode({'control_device':ID + '=' + Action + '=' + Value})
            if (debuging): xbmc.log('X10-Lights: HomeSeer, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = urllib.urlencode({'control_device':ID + '=ON'})
                if (debuging): xbmc.log('X10-Lights: HomeSeer, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = urllib.urlencode({'control_device':ID + '=OFF'})
                if (debuging): xbmc.log('X10-Lights: HomeSeer, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = urllib.urlencode({'control_device':ID + '=BRIGHT=' + Value})
                if (debuging): xbmc.log('X10-Lights: HomeSeer, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = urllib.urlencode({'control_device':ID + '=DIM=' + Value})
                if (debuging): xbmc.log('X10-Lights: HomeSeer, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: HomeSeer, No Action available!')

        HomeSeerRequest = urllib2.urlopen(URL, ActionData)
        if (debuging): xbmc.log('X10-Lights: HomeSeer, Request: ' + HomeSeerRequest)
        if (debuging): xbmc.log('X10-Lights: Action Send to HomeSeer')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: HomeSeer, XBMC ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

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
            if (debuging): xbmc.log('X10-Lights: tenHsServer, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '&a=ON'
                if (debuging): xbmc.log('X10-Lights: tenHsServer, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '&a=OFF'
                if (debuging): xbmc.log('X10-Lights: tenHsServer, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '&a=BRIGHT&s=' + Value + ''
                if (debuging): xbmc.log('X10-Lights: tenHsServer, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '&a=DIM&s=' + Value + ''
                if (debuging): xbmc.log('X10-Lights: tenHsServer, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: tenHsServer, No Action available!')

        if (debuging): xbmc.log('X10-Lights: tenHsServer, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to tenHsServer')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: tenHsServer, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

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
            if (debuging): xbmc.log('X10-Lights: Switch King, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '/turnon'
                if (debuging): xbmc.log('X10-Lights: Switch King, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '/turnoff'
                if (debuging): xbmc.log('X10-Lights: Switch King, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '/bright/' + Value + ''
                if (debuging): xbmc.log('X10-Lights: Switch King, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '/dim/' + Value + ''
                if (debuging): xbmc.log('X10-Lights: Switch King, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: Switch King, No Action available!')

        if (debuging): xbmc.log('X10-Lights: Switch King, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to Switch King')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: Switch King, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

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
            if (debuging): xbmc.log('X10-Lights: Thinking Home, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '&action=turnon'
                if (debuging): xbmc.log('X10-Lights: Thinking Home, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '&action=turnoff'
                if (debuging): xbmc.log('X10-Lights: Thinking Home, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '&action=bright&amount=' + Value
                if (debuging): xbmc.log('X10-Lights: Thinking Home, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '&action=dim&amount=' + Value
                if (debuging): xbmc.log('X10-Lights: Thinking Home, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: Thinking Home, No Action available!')

        if (debuging): xbmc.log('X10-Lights: Thinking Home, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to Thinking Home')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: Thinking Home, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

# HOMEWIZARD FUNCTION 
#This function Will execute the requested action in HomeWizard
def HomeWizard(URL, ID, Action, Value, FreeCmd):
    #HomeWizard STYLE
    #Example strings
    #http://<ip>/<password>/sw/<id>/on
    #http://<ip>/<password>/sw/<id>/off
    #http://<ip>/<password>/sw/dim/<id>/<dimlevel>

    try:
        if FreeCmd:
            ActionData = '/sw/' + Action + ID + '/' + Value
            if (debuging): xbmc.log('X10-Lights: HomeWizard, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = '/sw/' + ID + '/on'
                if (debuging): xbmc.log('X10-Lights: HomeWizard, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = '/sw/' + ID + '/off'
                if (debuging): xbmc.log('X10-Lights: HomeWizard, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = '/sw/dim/' + ID + '/' + Value
                if (debuging): xbmc.log('X10-Lights: HomeWizard, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = '/sw/dim/' + ID + '/' + Value
                if (debuging): xbmc.log('X10-Lights: HomeWizard, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: HomeWizard, No Action available!')

        if (debuging): xbmc.log('X10-Lights: HomeWizard, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to HomeWizard')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: HomeWizard, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue

# DOMOTICZ FUNCTION 
#This function Will execute the requested action in HomeSeer via tenHsServer
def Domoticz(URL, ID, Action, Value, FreeCmd):
    #Domoticz STYLE
    #Example strings
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/json.htm?type=command&param=switchlight&idx=' + my_devid + '&switchcmd=On&level=0')
    #urllib2.urlopen('http://' + my_ip + ':' + my_port + '/json.htm?type=command&param=switchlight&idx=' + my_devid + '&switchcmd=Off&level=0')
    #http://192.168.1.37:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=On&level=0
    #http://192.168.1.37:8080/json.htm?type=command&param=switchlight&idx=5&switchcmd=Off&level=0
    
    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
        if FreeCmd:
            ActionData = ID + '&a=' + Action + '&s=' + Value + ''
            if (debuging): xbmc.log('X10-Lights: Domoticz, Action: ' + Action + ', with value: ' + Value + '.')
        else:
            if Action == "ON":
                ActionData = ID + '&switchcmd=On&level=0'
                if (debuging): xbmc.log('X10-Lights: Domoticz, Switch lights or Device ON')
            elif Action == "OFF":
                ActionData = ID + '&switchcmd=Off&level=0'
                if (debuging): xbmc.log('X10-Lights: Domoticz, Switch lights or Device OFF')
            elif Action == "BRIGHT":
                ActionData = ID + '&switchcmd=On&level=' + Value + ''
                if (debuging): xbmc.log('X10-Lights: Domoticz, Brighten lights with ' + Value + '%')
            elif Action == "DIM":
                ActionData = ID + '&switchcmd=Off&level=' + Value + ''
                if (debuging): xbmc.log('X10-Lights: Domoticz, Dim lights with ' + Value + '%')
            else:
                if (debuging): xbmc.log('X10-Lights: Domoticz, No Action available!')

        if (debuging): xbmc.log('X10-Lights: Domoticz, URL: ' + URL + ActionData)
        X10CommanderRequest = urllib2.urlopen(URL + ActionData)
        if (debuging): xbmc.log('X10-Lights: Action Send to Domoticz')
        ReturnValue = "success"
    except:
        if (debuging): xbmc.log('X10-Lights: Domoticz, The ' + Action + ' Event Failed')
        ReturnValue = "fail"
    return ReturnValue


# EXECUTEACTION FUNCTION
def ExecuteAction(Application, URL, ID, Action, Value, FreeCmd):
    #This function is a simple selector 
    #It will call the correct Application to execute the desired action
    #This section should be expended with new aplication's as they come available
    if Application == "X10-COMMANDER":
        ReturnValue = X10Commander(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMESEER":
        ReturnValue = HomeSeer(URL, ID, Action, Value, FreeCmd)
    elif Application == "TENHSSERVER":
        ReturnValue = tenHsServer(URL, ID, Action, Value, FreeCmd)
    elif Application == "SWITCHKING":
        ReturnValue = SwitchKing(URL, ID, Action, Value, FreeCmd)
    elif Application == "THINKINGHOME":
        ReturnValue = ThinkingHome(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMEWIZARD":
        ReturnValue = HomeWizard(URL, ID, Action, Value, FreeCmd)
    elif Application == "DOMOTICZ":
        ReturnValue = Domoticz(URL, ID, Action, Value, FreeCmd)
    else:
        if (debuging): xbmc.log('X10-Lights: An unknown Device Aplication is selected!')
        ReturnValue = "failed"
    return ReturnValue

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

# MAINEVENTHANDLER FUNCTION
def MainEventHandler(Type):
    #This function is the MainEventHandler, 
    #It recieve the type of event that needs to be executed
    #The type of event comes from XMBC or the XBMC Player
    #for every active Device, where the event is enabled it will execute the action (ExecuteAction)
    
    #INITIALIZE
    DeviceCount = 1
    Application = DeviceApplication
    URL = DeviceURL
    
    if (debuging): 
        xbmc.log('X10-Lights: *************** Handeling an Event **************')
        xbmc.log('X10-Lights: Event Type = ' + str(Type))
    
    #Handle all Device's
    while (DeviceCount <= 5):
        #INITIALIZE per device
        ID = ""
        ActionEvent = ""
        ActionValue = ""
        ActionFreeCmd = ""
        ActionCall = ""
        ExecuteEvent = False
        if (DeviceCount <= 9):
            strCheckDeviceEnabled = "DEVID0" + str(DeviceCount) + "ENABLE"
            strCheckDeviceID = "DEVID0" + str(DeviceCount)
        else:
            strCheckDeviceEnabled = "DEVID" + str(DeviceCount) + "ENABLE"
            strCheckDeviceID = "DEVID" + str(DeviceCount)
        
        #Execute Event if Device is enabled
        if (str(__addon__.getSetting(strCheckDeviceEnabled)) == "true"):
            ID = __addon__.getSetting(strCheckDeviceID)
            
            #Retrieve specific device settings for the Event
            if Type == "X_Start":
                if (DeviceCount <= 9):
                    strXevStartEnabled = "XEVSTARTENABLE0" + str(DeviceCount)
                    strXevStartFree = "XEVSTARTFREE0" + str(DeviceCount)
                    strXevStartCmd = "XEVSTARTCMD0" + str(DeviceCount)
                    strXevStartVal = "XEVSTARTVAL0" + str(DeviceCount)
                    strXevStartPerc = "XEVSTARTPERC0" + str(DeviceCount)
                    strXevStart = "XEVSTART0" + str(DeviceCount)
                else:
                    strXevStartEnabled = "XEVSTARTENABLE" + str(DeviceCount)
                    strXevStartFree = "XEVSTARTFREE" + str(DeviceCount)
                    strXevStartCmd = "XEVSTARTCMD" + str(DeviceCount)
                    strXevStartVal = "XEVSTARTVAL" + str(DeviceCount)
                    strXevStartPerc = "XEVSTARTPERC" + str(DeviceCount)
                    strXevStart = "XEVSTART" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strXevStartEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strXevStartFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strXevStartCmd))
                        ActionValue = str(__addon__.getSetting(strXevStartVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strXevStart)))
                        ActionValue = str(__addon__.getSetting(strXevStartPerc))
                        ActionFreeCmd = False
            elif Type == "X_Stop":
                if (DeviceCount <= 9):
                    strXevStopEnabled = "XEVSTOPENABLE0" + str(DeviceCount)
                    strXevStopFree = "XEVSTOPFREE0" + str(DeviceCount)
                    strXevStopCmd = "XEVSTOPCMD0" + str(DeviceCount)
                    strXevStopVal = "XEVSTOPVAL0" + str(DeviceCount)
                    strXevStopPerc = "XEVSTOPPERC0" + str(DeviceCount)
                    strXevStop = "XEVSTOP0" + str(DeviceCount)
                else:
                    strXevStopEnabled = "XEVSTOPENABLE" + str(DeviceCount)
                    strXevStopFree = "XEVSTOPFREE" + str(DeviceCount)
                    strXevStopCmd = "XEVSTOPCMD" + str(DeviceCount)
                    strXevStopVal = "XEVSTOPVAL" + str(DeviceCount)
                    strXevStopPerc = "XEVSTOPPERC" + str(DeviceCount)
                    strXevStop = "XEVSTOP" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strXevStopEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strXevStopFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strXevStopCmd))
                        ActionValue = str(__addon__.getSetting(strXevStopVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strXevStop)))
                        ActionValue = str(__addon__.getSetting(strXevStopPerc))
                        ActionFreeCmd = False
            elif Type == "P_Start":
                if (DeviceCount <= 9):
                    strPevStartEnabled = "PEVSTARTENABLE0" + str(DeviceCount)
                    strPevStartFree = "PEVSTARTFREE0" + str(DeviceCount)
                    strPevStartCmd = "PEVSTARTCMD0" + str(DeviceCount)
                    strPevStartVal = "PEVSTARTVAL0" + str(DeviceCount)
                    strPevStartPerc = "PEVSTARTPERC0" + str(DeviceCount)
                    strPevStart = "PEVSTART0" + str(DeviceCount)
                else:
                    strPevStartEnabled = "PEVSTARTENABLE" + str(DeviceCount)
                    strPevStartFree = "PEVSTARTFREE" + str(DeviceCount)
                    strPevStartCmd = "PEVSTARTCMD" + str(DeviceCount)
                    strPevStartVal = "PEVSTARTVAL" + str(DeviceCount)
                    strPevStartPerc = "PEVSTARTPERC" + str(DeviceCount)
                    strPevStart = "PEVSTART" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevStartEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strPevStartFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strPevStartCmd))
                        ActionValue = str(__addon__.getSetting(strPevStartVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strPevStart)))
                        ActionValue = str(__addon__.getSetting(strPevStartPerc))
                        ActionFreeCmd = False
            elif Type == "P_Stop":
                if (DeviceCount <= 9):
                    strPevStopEnabled = "PEVSTOPENABLE0" + str(DeviceCount)
                    strPevStopFree = "PEVSTOPFREE0" + str(DeviceCount)
                    strPevStopCmd = "PEVSTOPCMD0" + str(DeviceCount)
                    strPevStopVal = "PEVSTOPVAL0" + str(DeviceCount)
                    strPevStopPerc = "PEVSTOPPERC0" + str(DeviceCount)
                    strPevStop = "PEVSTOP0" + str(DeviceCount)
                else:
                    strPevStopEnabled = "PEVSTOPENABLE" + str(DeviceCount)
                    strPevStopFree = "PEVSTOPFREE" + str(DeviceCount)
                    strPevStopCmd = "PEVSTOPCMD" + str(DeviceCount)
                    strPevStopVal = "PEVSTOPVAL" + str(DeviceCount)
                    strPevStopPerc = "PEVSTOPPERC" + str(DeviceCount)
                    strPevStop = "PEVSTOP" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevStopEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strPevStopFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strPevStopCmd))
                        ActionValue = str(__addon__.getSetting(strPevStopVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strPevStop)))
                        ActionValue = str(__addon__.getSetting(strPevStopPerc))
                        ActionFreeCmd = False
            elif Type == "P_Pause":
                if (DeviceCount <= 9):
                    strPevPauseEnabled = "PEVPAUSEENABLE0" + str(DeviceCount)
                    strPevPauseFree = "PEVPAUSEFREE0" + str(DeviceCount)
                    strPevPauseCmd = "PEVPAUSECMD0" + str(DeviceCount)
                    strPevPauseVal = "PEVPAUSEVAL0" + str(DeviceCount)
                    strPevPausePerc = "PEVPAUSEPERC0" + str(DeviceCount)
                    strPevPause = "PEVPAUSE0" + str(DeviceCount)
                else:
                    strPevPauseEnabled = "PEVPAUSEENABLE" + str(DeviceCount)
                    strPevPauseFree = "PEVPAUSEFREE" + str(DeviceCount)
                    strPevPauseCmd = "PEVPAUSECMD" + str(DeviceCount)
                    strPevPauseVal = "PEVPAUSEVAL" + str(DeviceCount)
                    strPevPausePerc = "PEVPAUSEPERC" + str(DeviceCount)
                    strPevPause = "PEVPAUSE" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevPauseEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strPevPauseFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strPevPauseCmd))
                        ActionValue = str(__addon__.getSetting(strPevPauseVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strPevPause)))
                        ActionValue = str(__addon__.getSetting(strPevPausePerc))
                        ActionFreeCmd = False
            elif Type == "P_End":
                if (DeviceCount <= 9):
                    strPevEndEnabled = "PEVENDENABLE0" + str(DeviceCount)
                    strPevEndFree = "PEVENDFREE0" + str(DeviceCount)
                    strPevEndCmd = "PEVENDCMD0" + str(DeviceCount)
                    strPevEndVal = "PEVENDVAL0" + str(DeviceCount)
                    strPevEndPerc = "PEVENDPERC0" + str(DeviceCount)
                    strPevEnd = "PEVEND0" + str(DeviceCount)
                else:
                    strPevEndEnabled = "PEVENDENABLE" + str(DeviceCount)
                    strPevEndFree = "PEVENDFREE" + str(DeviceCount)
                    strPevEndCmd = "PEVENDCMD" + str(DeviceCount)
                    strPevEndVal = "PEVENDVAL" + str(DeviceCount)
                    strPevEndPerc = "PEVENDPERC" + str(DeviceCount)
                    strPevEnd = "PEVEND" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevEndEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strPevEndFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strPevEndCmd))
                        ActionValue = str(__addon__.getSetting(strPevEndVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strPevEnd)))
                        ActionValue = str(__addon__.getSetting(strPevEndPerc))
                        ActionFreeCmd = False
            elif Type == "P_Resume":
                if (DeviceCount <= 9):
                    strPevResumeEnabled = "PEVRESUMEENABLE0" + str(DeviceCount)
                    strPevResumeFree = "PEVRESUMEFREE0" + str(DeviceCount)
                    strPevResumeCmd = "PEVRESUMECMD0" + str(DeviceCount)
                    strPevResumeVal = "PEVRESUMEVAL0" + str(DeviceCount)
                    strPevResumePerc = "PEVRESUMEPERC0" + str(DeviceCount)
                    strPevResume = "PEVRESUME0" + str(DeviceCount)
                else:
                    strPevResumeEnabled = "PEVRESUMEENABLE" + str(DeviceCount)
                    strPevResumeFree = "PEVRESUMEFREE" + str(DeviceCount)
                    strPevResumeCmd = "PEVRESUMECMD" + str(DeviceCount)
                    strPevResumeVal = "PEVRESUMEVAL" + str(DeviceCount)
                    strPevResumePerc = "PEVRESUMEPERC" + str(DeviceCount)
                    strPevResume = "PEVRESUME" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevResumeEnabled)) == "true"):
                    ExecuteEvent = True
                    if (str(__addon__.getSetting(strPevResumeFree)) == "true"):
                        #Free Command
                        ActionEvent = str(__addon__.getSetting(strPevResumeCmd))
                        ActionValue = str(__addon__.getSetting(strPevResumeVal))
                        ActionFreeCmd = True
                    else:
                        #Normal Command
                        ActionEvent = EventAction(str(__addon__.getSetting(strPevResume)))
                        ActionValue = str(__addon__.getSetting(strPevResumePerc))
                        ActionFreeCmd = False
            
            #Call to Execute the action on the device
            if (ExecuteEvent):
                ActionCall = ExecuteAction(Application, URL, ID, ActionEvent, ActionValue, ActionFreeCmd)
                if (debuging): 
                    xbmc.log('X10-Lights: Event Device ID = ' + str(ID))
                    xbmc.log('X10-Lights: Event Action    = ' + str(ActionEvent))
                    xbmc.log('X10-Lights: Event Value     = ' + str(ActionValue))
                    xbmc.log('X10-Lights: Event Free CMD  = ' + str(ActionFreeCmd))
                    xbmc.log('X10-Lights: *************************************************')
            else:
                ActionCall = "failed"
        
        DeviceCount = DeviceCount + 1
    return

# FUNCTIONS - LOGING
if (debuging): 
    xbmc.log('X10-Lights: ******************* X10-Lights ******************')
    xbmc.log('X10-Lights: Import of libraries is done')
    xbmc.log('X10-Lights: functions are initialized')
    xbmc.log('X10-Lights: *************************************************')

# FUNCTIONS - END

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
elif __addon__.getSetting("DEVAPP") == "5":
    DeviceApplication = "HOMEWIZARD" 
    #REMARK HomeWizard always needs a password (but not a username)  -  http://<ip>/<password>/  -  "http://" + ipadres + ":" + port + "/" + password;
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") +  '/' + __addon__.getSetting("PASS")
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT")  +  '/'
elif __addon__.getSetting("DEVAPP") == "6":
    DeviceApplication = "DOMOTICZ" 
    if (str(__addon__.getSetting("SECURITY")) == "true"):
        DeviceURL = 'http://' + __addon__.getSetting("USER") + ':' + __addon__.getSetting("PASS") + '@' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/json.htm?type=command&param=switchlight&idx='
    else:
        DeviceURL = 'http://' + __addon__.getSetting("IP") + ':' + __addon__.getSetting("PORT") + '/json.htm?type=command&param=switchlight&idx='
else:
    DeviceApplication = "UNKOWN"

# ADDON SHOW INFORMATION ABOUT ALL SETTINGS
if (debuging): 
    xbmc.log('X10-Lights: *************** Addon Host settings *************')
    xbmc.log('X10-Lights: IP number          : ' + str(__addon__.getSetting("IP")))
    xbmc.log('X10-Lights: PORT number        : ' + str(__addon__.getSetting("PORT")))
    xbmc.log('X10-Lights: *************************************************')
    xbmc.log('X10-Lights: Security: ' + str(__addon__.getSetting("SECURITY")))
    xbmc.log('X10-Lights: Base URL: ' + DeviceURL)

# ADDON START
if (debuging): 
    xbmc.log('X10-Lights: ******************** STARTUP ********************')
    xbmc.log('X10-Lights: *************************************************')

#START XBMC START Event
if (debuging): xbmc.log('X10-Lights: ****************** START EVENT ******************')

MainEventHandler("X_Start")

if (debuging): xbmc.log('X10-Lights: *************************************************')
#END XBMC START Event

# ADDON PLAYER
if (debuging): xbmc.log('X10-Lights: ****************** CLASS PLAYER *****************')
class MyPlayer(xbmc.Player) :
    if (debuging): xbmc.log('X10-Lights: Class player is opened')
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        if (debuging): xbmc.log('X10-Lights: Class player is initialized')

    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Start")
            if (debuging): xbmc.log('X10-Lights: PLAYBACK STARTED')

    def onPlayBackEnded(self):
        if (VIDEO == 1):
            MainEventHandler("P_End")
            if (debuging): xbmc.log('X10-Lights: PLAYBACK ENDED')

    def onPlayBackStopped(self):
        if (VIDEO == 1):
            MainEventHandler("P_Stop")
            if (debuging): xbmc.log('X10-Lights: PLAYBACK STOPPED')

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Pause")
            if (debuging): xbmc.log('X10-Lights: PLAYBACK PAUSED')

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Resume")
            if (debuging): xbmc.log('X10-Lights: PLAYBACK RESUMED')

player=MyPlayer()

while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0

    xbmc.sleep(1000)

if (xbmc.abortRequested):
    #START XBMC STOP Event
    if (debuging): xbmc.log('X10-Lights: ****************** STOP EVENT ******************')
    MainEventHandler("X_Stop")
    if (debuging): xbmc.log('X10-Lights: *************************************************')
    #END XBMC STOP Event
    #Execute XBMC STOP Event settings on Device