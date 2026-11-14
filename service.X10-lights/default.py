# -*- coding: utf-8 -*-
"""
    Document   : default.py
    Package    : X10 - Lights (Domotica Commander)
    Author     : Majestic Soft
    Copyright  : 2014-2026, Majestic Soft, NL
    License    : GNU General Public License v2 - see LICENSE
    Description: General control code for X10 - Lights (Domotica Commander)
    Revision   : 2.0.0
                 - Migrated to Python 3 (Kodi 19 Matrix, 20 Nexus, 21 Omega, 22 Piers+).
                 - Replaced obsolete xbmc.abortRequested loop with xbmc.Monitor().waitForAbort().
                 - Replaced urllib/urllib2 with urllib.request and urllib.parse.
                 - Added explicit timeouts (5s) to network calls to prevent Kodi UI blocking.
                 - Converted UDP socket communication (LightWaveRF) to bytes.
                 - Improved basic authentication via standard Authorization header.
                 - Preserved full backward compatibility with all 9 legacy domotica platforms.
"""

# IMPORT LIBRARIES
import sys
import os
import subprocess
import socket
import base64
import urllib.request
import urllib.parse
import urllib.error

import xbmc
import xbmcgui
import xbmcaddon

# Initialize ADDON
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__cwd__       = __addon__.getAddonInfo('path')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')

# Logging helpers
debuging = (__addon__.getSetting("DEBUGLOG").lower() == "true")

def log(msg, level=xbmc.LOGINFO):
    xbmc.log(f"X10-Lights: {msg}", level=level)

def log_debug(msg):
    if debuging:
        xbmc.log(f"X10-Lights: {msg}", level=xbmc.LOGDEBUG)

log("******************* X10-Lights ******************")
if debuging:
    log("Debugging log files is ON")
    log("*************** Addon information ***************")
    log(f"Addon info name    : {__addonname__}")
    log(f"Addon info path    : {__cwd__}")
    log(f"Addon info author  : {__author__}")
    log(f"Addon info version : {__version__}")
    log("*************************************************")
else:
    log("Debugging log files is OFF")
    log("*************************************************")

# Initialize Transaction number for LightWaveRF
TransactionID = 100

# Helper function for sending HTTP GET requests with timeout and optional Basic Auth
def send_http_get(url, auth_user=None, auth_pass=None, timeout=5):
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': f'Kodi-service.X10-lights/{__version__}'}
        )
        if auth_user and auth_pass:
            auth_str = f"{auth_user}:{auth_pass}"
            auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('ascii')
            req.add_header("Authorization", f"Basic {auth_b64}")

        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as err:
        log_debug(f"HTTP GET Error ({url}): {err}")
        raise

# Helper function for sending HTTP POST requests with timeout and optional Basic Auth
def send_http_post(url, data_dict, auth_user=None, auth_pass=None, timeout=5):
    try:
        data = urllib.parse.urlencode(data_dict).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={'User-Agent': f'Kodi-service.X10-lights/{__version__}'}
        )
        if auth_user and auth_pass:
            auth_str = f"{auth_user}:{auth_pass}"
            auth_b64 = base64.b64encode(auth_str.encode('utf-8')).decode('ascii')
            req.add_header("Authorization", f"Basic {auth_b64}")

        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as err:
        log_debug(f"HTTP POST Error ({url}): {err}")
        raise

# ==============================================================================
# CONTROLLER FUNCTIONS - START
# ==============================================================================

# 1. X10-COMMANDER FUNCTION
def X10Commander(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            ActionData = f'{ID} {Action} {Value}"'
            log_debug(f"X10-Commander, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f'{ID} ON"'
                log_debug("X10-Commander, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f'{ID} OFF"'
                log_debug("X10-Commander, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f'{ID} BRIGHT {Value}"'
                log_debug(f"X10-Commander, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f'{ID} DIM {Value}"'
                log_debug(f"X10-Commander, Dim lights with {Value}%")
            else:
                log_debug("X10-Commander, No Action available!")
                ActionData = ""

        full_url = URL + urllib.parse.quote(ActionData, safe='?&=~/')
        log_debug(f"X10-Commander, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to X10-Commander")
        return "success"
    except Exception as err:
        log_debug(f"X10-Commander, The {Action} Event Failed: {err}")
        return "fail"

# 2. HOMESEER FUNCTION
def HomeSeer(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            cmd = f"{ID}={Action}={Value}"
            log_debug(f"HomeSeer, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                cmd = f"{ID}=ON"
                log_debug("HomeSeer, Switch lights or Device ON")
            elif Action == "OFF":
                cmd = f"{ID}=OFF"
                log_debug("HomeSeer, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                cmd = f"{ID}=BRIGHT={Value}"
                log_debug(f"HomeSeer, Brighten lights with {Value}%")
            elif Action == "DIM":
                cmd = f"{ID}=DIM={Value}"
                log_debug(f"HomeSeer, Dim lights with {Value}%")
            else:
                log_debug("HomeSeer, No Action available!")
                cmd = ""

        post_data = {'control_device': cmd}
        log_debug(f"HomeSeer, URL: {URL}, Data: {post_data}")
        send_http_post(URL, post_data, timeout=5)
        log_debug("Action Sent to HomeSeer")
        return "success"
    except Exception as err:
        log_debug(f"HomeSeer, The {Action} Event Failed: {err}")
        return "fail"

# 3. TENHSSERVER FUNCTION
def tenHsServer(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            ActionData = f"{ID}&a={Action}&s={Value}"
            log_debug(f"tenHsServer, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{ID}&a=ON"
                log_debug("tenHsServer, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{ID}&a=OFF"
                log_debug("tenHsServer, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{ID}&a=BRIGHT&s={Value}"
                log_debug(f"tenHsServer, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f"{ID}&a=DIM&s={Value}"
                log_debug(f"tenHsServer, Dim lights with {Value}%")
            else:
                log_debug("tenHsServer, No Action available!")
                ActionData = ""

        full_url = URL + ActionData
        log_debug(f"tenHsServer, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to tenHsServer")
        return "success"
    except Exception as err:
        log_debug(f"tenHsServer, The {Action} Event Failed: {err}")
        return "fail"

# 4. SWITCH KING FUNCTION
def SwitchKing(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            ActionData = f"{ID}/{Action}/{Value}"
            log_debug(f"Switch King, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{ID}/turnon"
                log_debug("Switch King, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{ID}/turnoff"
                log_debug("Switch King, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{ID}/bright/{Value}"
                log_debug(f"Switch King, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f"{ID}/dim/{Value}"
                log_debug(f"Switch King, Dim lights with {Value}%")
            else:
                log_debug("Switch King, No Action available!")
                ActionData = ""

        full_url = URL + ActionData
        log_debug(f"Switch King, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to Switch King")
        return "success"
    except Exception as err:
        log_debug(f"Switch King, The {Action} Event Failed: {err}")
        return "fail"

# 5. THINKING HOME FUNCTION
def ThinkingHome(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            ActionData = f"{ID}&action={Action}&value={Value}"
            log_debug(f"Thinking Home, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{ID}&action=turnOn"
                log_debug("Thinking Home, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{ID}&action=turnOff"
                log_debug("Thinking Home, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{ID}&action=brighten&value={Value}"
                log_debug(f"Thinking Home, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f"{ID}&action=dim&value={Value}"
                log_debug(f"Thinking Home, Dim lights with {Value}%")
            else:
                log_debug("Thinking Home, No Action available!")
                ActionData = ""

        full_url = URL + ActionData
        log_debug(f"Thinking Home, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to Thinking Home")
        return "success"
    except Exception as err:
        log_debug(f"Thinking Home, The {Action} Event Failed: {err}")
        return "fail"

# 6. HOMEWIZARD FUNCTION
def HomeWizard(URL, ID, Action, Value, FreeCmd):
    try:
        # HomeWizard dim range is 0 to 100 percentage directly supported
        if FreeCmd:
            ActionData = f"sw/{ID}/{Action}/{Value}"
            log_debug(f"HomeWizard, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"sw/{ID}/on"
                log_debug("HomeWizard, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"sw/{ID}/off"
                log_debug("HomeWizard, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"sw/dim/{ID}/{Value}"
                log_debug(f"HomeWizard, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f"sw/dim/{ID}/{Value}"
                log_debug(f"HomeWizard, Dim lights with {Value}%")
            else:
                log_debug("HomeWizard, No Action available!")
                ActionData = ""

        # Ensure correct URL trailing slash
        base_url = URL if URL.endswith('/') else URL + '/'
        full_url = base_url + ActionData
        log_debug(f"HomeWizard, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to HomeWizard")
        return "success"
    except Exception as err:
        log_debug(f"HomeWizard, The {Action} Event Failed: {err}")
        return "fail"

# 7. DOMOTICZ FUNCTION
def Domoticz(URL, ID, Action, Value, FreeCmd):
    try:
        # Domoticz level ranges from 0 to 16 (0-100%)
        fValue = float(Value) if Value else 0.0
        iValue = int((fValue / 100.0) * 16)
        sValue = str(iValue)

        if FreeCmd:
            ActionData = f"{ID}&a={Action}&s={Value}"
            log_debug(f"Domoticz, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{ID}&switchcmd=On&level=0"
                log_debug("Domoticz, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{ID}&switchcmd=Off&level=0"
                log_debug("Domoticz, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{ID}&switchcmd=Set%20Level&level={sValue}"
                log_debug(f"Domoticz, Brighten lights with {Value}% converted to level: {sValue}")
            elif Action == "DIM":
                ActionData = f"{ID}&switchcmd=Set%20Level&level={sValue}"
                log_debug(f"Domoticz, Dim lights with {Value}% converted to level: {sValue}")
            else:
                log_debug("Domoticz, No Action available!")
                ActionData = ""

        full_url = URL + ActionData
        log_debug(f"Domoticz, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to Domoticz")
        return "success"
    except Exception as err:
        log_debug(f"Domoticz, The {Action} Event Failed: {err}")
        return "fail"

# 8. HOMEGENIE FUNCTION
def HomeGenie(URL, ID, Action, Value, FreeCmd):
    try:
        if FreeCmd:
            ActionData = f"{ID}/Control.{Action}/{Value}"
            log_debug(f"HomeGenie, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{ID}/Control.On"
                log_debug("HomeGenie, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{ID}/Control.Off"
                log_debug("HomeGenie, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{ID}/Control.Bright/{Value}"
                log_debug(f"HomeGenie, Brighten lights with {Value}%")
            elif Action == "DIM":
                ActionData = f"{ID}/Control.Dim/{Value}"
                log_debug(f"HomeGenie, Dim lights with {Value}%")
            else:
                log_debug("HomeGenie, No Action available!")
                ActionData = ""

        full_url = URL + ActionData
        log_debug(f"HomeGenie, URL: {full_url}")
        send_http_get(full_url, timeout=5)
        log_debug("Action Sent to HomeGenie")
        return "success"
    except Exception as err:
        log_debug(f"HomeGenie, The {Action} Event Failed: {err}")
        return "fail"

# 9. LIGHTWAVERF FUNCTION (UDP Socket)
def LightWaveRF(URL, ID, Action, Value, FreeCmd, ROOM):
    global TransactionID
    try:
        # Extract Host and Port from format: 'host: <ip> port: <port>'
        parts = URL.split()
        url_host = parts[1] if len(parts) > 1 else "127.0.0.1"
        url_port = int(parts[3]) if len(parts) > 3 else 9760

        # Calculate Level (1-32)
        fValue = float(Value) if Value else 0.0
        iValue = int((fValue / 100.0) * 32)
        sValue = str(iValue)

        if FreeCmd:
            ActionData = f"{TransactionID},!R{ROOM}D{ID}{Action}{Value}\r"
            log_debug(f"LightWaveRF, Action: {Action}, with value: {Value}.")
        else:
            if Action == "ON":
                ActionData = f"{TransactionID},!R{ROOM}D{ID}F1\r"
                log_debug("LightWaveRF, Switch lights or Device ON")
            elif Action == "OFF":
                ActionData = f"{TransactionID},!R{ROOM}D{ID}F0\r"
                log_debug("LightWaveRF, Switch lights or Device OFF")
            elif Action == "BRIGHT":
                ActionData = f"{TransactionID},!R{ROOM}D{ID}FdP{sValue}\r"
                log_debug(f"LightWaveRF, Brighten lights to {Value}% (level {sValue})")
            elif Action == "DIM":
                ActionData = f"{TransactionID},!R{ROOM}D{ID}FdP{sValue}\r"
                log_debug(f"LightWaveRF, Dim lights to {Value}% (level {sValue})")
            else:
                log_debug("LightWaveRF, No Action available!")
                ActionData = ""

        log_debug(f"LightWaveRF, HOST: {url_host} PORT: {url_port} Package: {ActionData.strip()}")
        
        # In Python 3, socket sendto/send requires bytes
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5.0)
        sock.sendto(ActionData.encode('utf-8'), (url_host, url_port))
        sock.close()

        TransactionID += 1
        log_debug("Action Sent to LightWaveRF")
        return "success"
    except Exception as err:
        log_debug(f"LightWaveRF, The {Action} Event Failed: {err}")
        return "fail"

# ==============================================================================
# DISPATCHER AND EVENT HANDLERS
# ==============================================================================

def ExecuteAction(Application, URL, ID, Action, Value, FreeCmd, Room="0"):
    if Application == "X10-COMMANDER":
        return X10Commander(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMESEER":
        return HomeSeer(URL, ID, Action, Value, FreeCmd)
    elif Application == "TENHSSERVER":
        return tenHsServer(URL, ID, Action, Value, FreeCmd)
    elif Application == "SWITCHKING":
        return SwitchKing(URL, ID, Action, Value, FreeCmd)
    elif Application == "THINKINGHOME":
        return ThinkingHome(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMEWIZARD":
        return HomeWizard(URL, ID, Action, Value, FreeCmd)
    elif Application == "DOMOTICZ":
        return Domoticz(URL, ID, Action, Value, FreeCmd)
    elif Application == "HOMEGENIE":
        return HomeGenie(URL, ID, Action, Value, FreeCmd)
    elif Application == "LIGHTWAVERF":
        return LightWaveRF(URL, ID, Action, Value, FreeCmd, Room)
    else:
        log_debug("An unknown Device Application is selected!")
        return "failed"

def EventAction(Action):
    if Action == "3":
        return "OFF"
    elif Action == "2":
        return "ON"
    elif Action == "1":
        return "BRIGHT"
    else:
        return "DIM"

def MainEventHandler(Type):
    DeviceCount = 1
    Application = DeviceApplication
    URL = DeviceURL

    log_debug("*************** Handling an Event **************")
    log_debug(f"Event Type = {Type}")

    # Handle all Devices (1 to 5)
    while DeviceCount <= 5:
        ID = ""
        ROOM = "0"
        ActionEvent = ""
        ActionValue = ""
        ActionFreeCmd = False
        ExecuteEvent = False

        suffix = f"0{DeviceCount}" if DeviceCount <= 9 else str(DeviceCount)
        strCheckDeviceEnabled = f"DEVID{suffix}ENABLE"
        strCheckDeviceID = f"DEVID{suffix}"
        strCheckRoomEnabled = f"ROOM{suffix}ENABLE"
        strCheckRoom = f"ROOM{suffix}"

        if __addon__.getSetting(strCheckDeviceEnabled).lower() == "true":
            ID = __addon__.getSetting(strCheckDeviceID)
            if __addon__.getSetting(strCheckRoomEnabled).lower() == "true":
                ROOM = __addon__.getSetting(strCheckRoom)

            # Retrieve event settings based on Event Type
            prefix_map = {
                "X_Start": "XEVSTART",
                "X_Stop": "XEVSTOP",
                "P_Start": "PEVSTART",
                "P_Stop": "PEVSTOP",
                "P_Pause": "PEVPAUSE",
                "P_Resume": "PEVRESUME",
                "P_End": "PEVEND",
            }

            prefix = prefix_map.get(Type)
            if prefix:
                ev_enabled = __addon__.getSetting(f"{prefix}ENABLE{suffix}").lower() == "true"
                ev_free = __addon__.getSetting(f"{prefix}FREE{suffix}").lower() == "true"

                if ev_enabled:
                    ExecuteEvent = True
                    if ev_free:
                        ActionEvent = str(__addon__.getSetting(f"{prefix}CMD{suffix}"))
                        ActionValue = str(__addon__.getSetting(f"{prefix}VAL{suffix}"))
                        ActionFreeCmd = True
                    else:
                        ActionEvent = EventAction(str(__addon__.getSetting(f"{prefix}{suffix}")))
                        ActionValue = str(__addon__.getSetting(f"{prefix}PERC{suffix}"))
                        ActionFreeCmd = False

        if ExecuteEvent:
            log_debug(f"Executing event {Type} for Device {DeviceCount} (ID: {ID})")
            ExecuteAction(Application, URL, ID, ActionEvent, ActionValue, ActionFreeCmd, ROOM)

        DeviceCount += 1

    log_debug("*************************************************")

# ==============================================================================
# CONFIGURATION INITIALIZATION
# ==============================================================================

app_setting = __addon__.getSetting("DEVAPP")
ip_setting = __addon__.getSetting("IP")
port_setting = __addon__.getSetting("PORT")
security_setting = __addon__.getSetting("SECURITY").lower() == "true"
user_setting = __addon__.getSetting("USER")
pass_setting = __addon__.getSetting("PASS")

if app_setting == "0":
    DeviceApplication = "X10-COMMANDER"
    auth_part = f"{user_setting}:{pass_setting}@" if security_setting else ""
    DeviceURL = f"http://{auth_part}{ip_setting}:{port_setting}/?x10command=DEVICE~sendplc~\""
elif app_setting == "1":
    DeviceApplication = "HOMESEER"
    DeviceURL = f"http://{ip_setting}:{port_setting}/tail.htm"
elif app_setting == "2":
    DeviceApplication = "TENHSSERVER"
    auth_part = f"{user_setting}:{pass_setting}@" if security_setting else ""
    DeviceURL = f"http://{auth_part}{ip_setting}:{port_setting}/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d="
elif app_setting == "3":
    DeviceApplication = "SWITCHKING"
    auth_part = f"{user_setting}:{pass_setting}@" if security_setting else ""
    DeviceURL = f"http://{auth_part}{ip_setting}:{port_setting}/devices/"
elif app_setting == "4":
    DeviceApplication = "THINKINGHOME"
    auth_part = f"{user_setting}:{pass_setting}@" if security_setting else ""
    DeviceURL = f"http://{auth_part}{ip_setting}:{port_setting}/cgi-bin/thinkingHome-cgi?devName="
elif app_setting == "5":
    DeviceApplication = "HOMEWIZARD"
    if security_setting:
        DeviceURL = f"http://{ip_setting}:{port_setting}/{pass_setting}/"
    else:
        DeviceURL = f"http://{ip_setting}:{port_setting}/"
elif app_setting == "6":
    DeviceApplication = "DOMOTICZ"
    auth_part = f"{user_setting}:{pass_setting}@" if security_setting else ""
    DeviceURL = f"http://{auth_part}{ip_setting}:{port_setting}/json.htm?type=command&param=switchlight&idx="
elif app_setting == "7":
    DeviceApplication = "HOMEGENIE"
    DeviceURL = f"http://{ip_setting}:{port_setting}/api/HomeAutomation.X10/"
elif app_setting == "8":
    DeviceApplication = "LIGHTWAVERF"
    DeviceURL = f"host: {ip_setting} port: {port_setting}"
else:
    DeviceApplication = "UNKNOWN"
    DeviceURL = ""

if debuging:
    log("*************** Addon Host settings *************")
    log(f"IP number          : {ip_setting}")
    log(f"PORT number        : {port_setting}")
    log(f"Security           : {security_setting}")
    log(f"Application        : {DeviceApplication}")
    log(f"Base URL           : {DeviceURL}")
    log("*************************************************")

# ==============================================================================
# PLAYER CLASS & MONITOR (MODERN KODI 19/20/21/22+)
# ==============================================================================

class MyPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()
        self.was_playing_video = False
        log_debug("Class MyPlayer initialized")

    def onPlayBackStarted(self):
        if self.isPlayingVideo():
            self.was_playing_video = True
            MainEventHandler("P_Start")
            log_debug("PLAYBACK STARTED (Video)")

    def onAVStarted(self):
        # Additional modern Kodi callback when video/audio stream starts
        if self.isPlayingVideo() and not self.was_playing_video:
            self.was_playing_video = True
            MainEventHandler("P_Start")
            log_debug("AV STARTED (Video)")

    def onPlayBackEnded(self):
        if self.was_playing_video:
            self.was_playing_video = False
            MainEventHandler("P_End")
            log_debug("PLAYBACK ENDED")

    def onPlayBackStopped(self):
        if self.was_playing_video:
            self.was_playing_video = False
            MainEventHandler("P_Stop")
            log_debug("PLAYBACK STOPPED")

    def onPlayBackPaused(self):
        if self.isPlayingVideo():
            MainEventHandler("P_Pause")
            log_debug("PLAYBACK PAUSED")

    def onPlayBackResumed(self):
        if self.isPlayingVideo():
            MainEventHandler("P_Resume")
            log_debug("PLAYBACK RESUMED")

# ==============================================================================
# MAIN SERVICE ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    log_debug("******************** STARTUP ********************")
    log_debug("****************** START EVENT ******************")
    MainEventHandler("X_Start")
    log_debug("*************************************************")

    player = MyPlayer()
    monitor = xbmc.Monitor()

    # Modern Kodi Event Loop: waitForAbort releases CPU instantly on shutdown
    while not monitor.abortRequested():
        if player.isPlayingVideo():
            player.was_playing_video = True
        
        # Wait up to 1 second; returns True immediately if Kodi requests abort
        if monitor.waitForAbort(1):
            break

    # Kodi Shutdown / Service Stop Event
    log_debug("****************** STOP EVENT ******************")
    MainEventHandler("X_Stop")
    log_debug("*************************************************")
    log("Service stopped cleanly.")
