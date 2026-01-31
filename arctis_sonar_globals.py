import json
import time
from subprocess import Popen, PIPE
from threading import Event

from PyQt6.QtCore import *
import sys
import os
import datetime
import uuid
import logging
from enum import Enum
import pulsectl

pulse = pulsectl.Pulse('ArctisSonar_GUI')

class ArctisDevice:
    def __init__(self, name, idVendor, idProduct):
        self.name = name
        self.idVendor = idVendor
        self.idProduct = idProduct
        self.isActive = False

class LogLevel(Enum):
    Info = "INFO"
    Warning = "WARNING"
    Error = "ERROR"
    Exception = "EXCEPTION"
    Debug = "DEBUG"

class ArctisSonarGUI(QObject):
    def __init__(self, *args, **kwargs):
        super(ArctisSonarGUI, self).__init__(*args, **kwargs)

        self.buildVersion = "0.1.2"
        self.buildDate = datetime.datetime(
            year=2026,
            month=1,
            day=31
        )

        self.organisationName = "mngazy"
        self.devMode = True
        self.applicationName = "ArctisSonar GUI"

        self.logger:logging.Logger = None

        self.appDocDirectory = ""
        self.applicationLoggerDirectory = ""
        self.appSessionsDirectory = ""
        self.sessionDirectory = ""
        self.documentationDirectory = ""
        self.settings: QSettings = None
        self.createAppDocFolder()
        self.createApplicationLogger()

    def createApplicationLogger(self):
        self.applicationLoggerDirectory = f"{self.appDocDirectory}/AppLogFiles"
        logging.basicConfig(filename=f"{self.applicationLoggerDirectory}/{datetime.datetime.now().strftime("%m_%d_%Y__%H_%M_%S")}.log", filemode='a+',
                            format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', datefmt='%H:%M:%S',
                            level=logging.DEBUG)
        logging.info("Starting Application")
        logging.info("Log Created")
        logging.info(f"{self.applicationName} Version: {self.buildVersion}")
        logging.info(f"Platform: {sys.platform}")

        logging.info("\n\n")
        logging.info("Starting Application")
        logging.info("\n\n")
        self.logger = logging.getLogger("appLogger")
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        errorHandler = logging.StreamHandler(sys.stderr)
        errorHandler.setLevel(logging.ERROR)
        formatter = logging.Formatter('\n\nERROR: %(asctime)s - %(process)d - %(levelname)s - %(message)s\n\n')
        errorHandler.setFormatter(formatter)
        self.logger.addHandler(errorHandler)

    def log(self,level:LogLevel,message:str):
        levelInt = logging.getLevelNamesMapping()[level.value]
        self.logger.log(levelInt,message)

    def createAppDocFolder(self):
        self.appDocDirectory = "%s/%s" % (
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),self.applicationName)
        self.applicationLoggerDirectory = f"{self.appDocDirectory}/AppLogFiles"
        self.appSessionsDirectory = f"{self.appDocDirectory}/Sessions"
        if not os.path.isdir(self.appDocDirectory):
            os.mkdir(self.appDocDirectory)
            os.mkdir(self.applicationLoggerDirectory)
            os.mkdir(self.appSessionsDirectory)
            self.createSettings()

    def createSettings(self):
        self.settings = QSettings(self.organisationName,self.applicationName)

        self.settings.beginGroup("Application Settings")
        self.settings.setValue("theme","dark")
        self.settings.setValue("firstTimeSetup", True)

        self.settings.setValue("enableSonar", True) ## enable sonar on startup
        self.settings.setValue("logChatMix", False)
        self.settings.endGroup()

        self.settings.beginGroup("UI")
        self.settings.setValue("theme","Dark Theme")
        self.settings.endGroup()

        self.settings.beginGroup("Device Details")
        self.settings.setValue("deviceIDVendor", None) ## last selected device
        self.settings.setValue("deviceIDProduct", None) ## last selected device
        self.settings.endGroup()

        self.settings.beginGroup("Sink Details")
        self.settings.setValue("changeAudioDeviceOnStartup", True)  ## change the audio device automatically to audio virtual sinks on startup
        self.settings.endGroup()

        self.settings.beginGroup("Developer Settings")
        self.settings.endGroup()

        self.settings.beginGroup("Application Info")
        self.settings.setValue("lastRunningVersion",self.buildVersion)
        self.settings.setValue("buildDate", self.buildDate)
        self.settings.endGroup()

        self.settings.sync()

    def updateApplicationSettings(self,group,key, value):
        self.settings = QSettings(self.organisationName,self.applicationName)
        self.settings.beginGroup(group)
        self.settings.setValue(key, value)
        self.settings.endGroup()
        self.settings.sync()

    def retrieveApplicationSetting(self,group,key, defaultValue=None):
        self.settings = QSettings(self.organisationName,self.applicationName)
        self.settings.beginGroup(group)
        value = self.settings.value(key)
        if value is None:
            # self.log(LogLevel.Info, f"No setting value found for {group}:{key}. Setting to default: {defaultValue}")
            self.settings.setValue(key,defaultValue)
            value = defaultValue
        self.settings.endGroup()
        return value

    def returnBoolSetting(self, group,key, defaultValue=None):
        value = self.retrieveApplicationSetting(group,key,defaultValue)
        if type(value) != bool:
            return eval(value.title())
        return value

    def returnApplicationPath(self):
        application_path = ""
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
            os.chdir(application_path)
        else:
            application_path = os.path.dirname(__file__)
        application_path = application_path + "/"
        return application_path

    def addHandlerToLogger(self, handler):
        self.logger.addHandler(handler)



arctisSonarGUI = ArctisSonarGUI()

class ArctisSonarListenerThread(QThread):
    onMixerChanged = pyqtSignal(int, int)
    onSelectedDeviceChanged = pyqtSignal(object)
    onAvailableDevicesChanged = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(ArctisSonarListenerThread, self).__init__(*args, **kwargs)

        arctisSonarGUI.log(LogLevel.Info, "Initializing ArctisSonarListener")

        self.currentDevice:ArctisDevice|None = None
        self.arctisDevices: [ArctisDevice] = []

        self.isHeadsetControlInstalled = False

        self.originalSink = None

        self.quitEvent = Event()
        self.quitEvent.clear()

        self.arctisGameSinkName = "ArctisSonar_Game"
        self.arctisChatSinkName = "ArctisSonar_Chat"

        self.chatVolumeLevel = 100
        self.gameVolumeLevel = 100

        self.checkHeadsetControlInstalled()
        self.getAllArctisDevices()

        if self.isHeadsetControlInstalled:
            deviceIDVendor, deviceIDProduct = self.returnLastSavedDevice()
            if deviceIDVendor is not None and deviceIDProduct is not None:
                device = self.checkDeviceConnected(deviceIDVendor, deviceIDProduct)
                if device is not None:
                    self.setDeviceAsActive(device)
                else:
                    self.currentDevice = None

    def start(self, priority = ...):
        self.checkHeadsetControlInstalled()
        if self.isHeadsetControlInstalled:

            self.createVirtualSinks()
            deviceIDVendor, deviceIDProduct = self.returnLastSavedDevice()
            if deviceIDVendor is not None and deviceIDProduct is not None:
                device = self.checkDeviceConnected(deviceIDVendor, deviceIDProduct)
                if device is not None:
                    self.setDeviceAsActive(device)
                else:
                    self.currentDevice = None
            self.onSelectedDeviceChanged.emit(self.currentDevice)
            self.quitEvent.clear()
            super().start(priority)

    def checkHeadsetControlInstalled(self):
        stdout = os.popen("headsetcontrol -m -o json").readlines()
        if stdout != []:
            self.isHeadsetControlInstalled = True
            arctisSonarGUI.log(LogLevel.Info, "Headset Control Installation Confirmed")
        else:
            arctisSonarGUI.log(LogLevel.Info, "Headset Control was not installed or is not working properly. 'headsetcontrol -m -o json' reported an error")


    def getAllArctisDevices(self):
        self.arctisDevices = []
        if self.isHeadsetControlInstalled:
            stdout = os.popen("headsetcontrol -m -o json").readlines()
            headsetControlOutput = "\n".join(stdout)
            headsetControlOutput = json.loads(headsetControlOutput)

            for device in headsetControlOutput["devices"]:
                if device.get("chatmix",None) is not None and type(device.get("chatmix")) == int:
                    self.arctisDevices.append(ArctisDevice(
                        name=device["device"],
                        idVendor=int(device["id_vendor"],16),
                        idProduct=int(device["id_product"],16),
                    ))
        else:
            arctisSonarGUI.log(LogLevel.Info,
                               "Headset Control was not installed or is not working properly. 'headsetcontrol -m -o json' reported an error")

        self.onAvailableDevicesChanged.emit(self.arctisDevices)
        return self.arctisDevices

    def createVirtualSinks(self):
        self.originalSink = pulse.sink_default_get()
        print("original sink", self.originalSink)
        self.destroyCreatedVirtualSinks()
        arctisDeviceSink = self.returnArctisDeviceSink()
        if arctisDeviceSink:
            try:
                arctisSonarGUI.log(LogLevel.Info, "Creating Virtual Sink Nodes")

                os.system("""pw-cli create-node adapter '{ 
                            factory.name=support.null-audio-sink 
                            node.name=%s 
                            node.description="%s" 
                            media.class=Audio/Sink 
                            monitor.channel-volumes=true 
                            object.linger=true 
                            audio.position=[FL FR]
                            }' 1>/dev/null
                        """ % (self.arctisGameSinkName, self.arctisGameSinkName))

                os.system("""pw-cli create-node adapter '{ 
                            factory.name=support.null-audio-sink 
                            node.name=%s
                            node.description="%s" 
                            media.class=Audio/Sink 
                            monitor.channel-volumes=true 
                            object.linger=true 
                            audio.position=[FL FR]
                            }' 1>/dev/null
                        """ % (self.arctisChatSinkName, self.arctisChatSinkName))

                arctisSonarGUI.log(LogLevel.Info, "Created Virtual Sink Nodes")

            except Exception as e:
                arctisSonarGUI.log(LogLevel.Exception, f"""Failed to create Virtual Sink Nodes: {e}""")
                self.kill()

            time.sleep(0.7) ## wait for one second to create the virtual sinks
            gameSinkCreated, chatSinkCreated = self.returnVirtualSinks()

            if gameSinkCreated and chatSinkCreated:

                # route the virtual sink's L&R channels to the default system output's LR
                try:
                    arctisSonarGUI.log(LogLevel.Info, f"Linking Sinks to Arctis Device Sink {arctisDeviceSink}")

                    arctisSonarGUI.log(LogLevel.Info, f"Linking Game Sink")
                    os.system(f'pw-link "{self.arctisGameSinkName}:monitor_FL" '
                              f'"{arctisDeviceSink}:playback_FL" 1>/dev/null')

                    os.system(f'pw-link "{self.arctisGameSinkName}:monitor_FR" '
                              f'"{arctisDeviceSink}:playback_FR" 1>/dev/null')

                    arctisSonarGUI.log(LogLevel.Info, f"Linking Chat Sink")
                    os.system(f'pw-link "{self.arctisChatSinkName}:monitor_FL" '
                              f'"{arctisDeviceSink}:playback_FL" 1>/dev/null')

                    os.system(f'pw-link "{self.arctisChatSinkName}:monitor_FR" '
                              f'"{arctisDeviceSink}:playback_FR" 1>/dev/null')

                except Exception as e:
                    arctisSonarGUI.log(LogLevel.Exception, f"Failed to create Virtual Sinks : {e}")

                arctisSonarGUI.log(LogLevel.Info, "Linked Virtual Sink Nodes to Arctis Device Sink")
                changeDeviceOnStartup = arctisSonarGUI.returnBoolSetting("Sink Details",
                                                                                  "changeAudioDeviceOnStartup", True)
                if changeDeviceOnStartup:
                    os.system(f'pactl set-default-sink {self.arctisGameSinkName}')
                else:
                    os.system(f'pactl set-default-sink {self.originalSink}')

    def returnVirtualSinks(self):
        sink_list = pulse.sink_list()
        gameSinkFound = False
        chatSinkFound = False
        for sink in sink_list:
            if sink.name == self.arctisGameSinkName:
                gameSinkFound = True

            elif sink.name == self.arctisChatSinkName:
                chatSinkFound = True

        return gameSinkFound, chatSinkFound

    def destroyCreatedVirtualSinks(self):
        sink_list = pulse.sink_list()
        for sink in sink_list:
            if sink.name == self.arctisGameSinkName or sink.name == self.arctisChatSinkName:
                os.system(f"pw-cli destroy {sink.name} 2>/dev/null")
                arctisSonarGUI.log(LogLevel.Info, f"""Destroyed node adapter - {sink.name}""")

    def returnArctisDeviceSink(self):
        sink_list = pulse.sink_list()
        name = None
        for sink in sink_list:
            if "steelseries" in sink.name.lower() and "arctis" in sink.name.lower() and "analog" in sink.name.lower():
                name = sink.name
        return name

    def returnLastSavedDevice(self):
        deviceIDVendor = arctisSonarGUI.retrieveApplicationSetting("Device Details", "deviceIDVendor", None)
        deviceIDProduct = arctisSonarGUI.retrieveApplicationSetting("Device Details", "deviceIDProduct", None)

        if deviceIDVendor and deviceIDProduct is not None:
            deviceIDVendor = int(deviceIDVendor)
            deviceIDProduct = int(deviceIDProduct)

        return deviceIDVendor, deviceIDProduct

    def returnCurrentDevice(self):
        return self.currentDevice

    def checkDeviceConnected(self, idVendor, idProduct):
        if idVendor is not None and idProduct is not None:
            attempts = 3
            while attempts > 0:
                indexOfSelectedDevice = [i for i, n in enumerate(self.arctisDevices) if n.idVendor == idVendor and n.idProduct == idProduct]
                if indexOfSelectedDevice:
                    attempts = -1
                    return self.arctisDevices[indexOfSelectedDevice[0]]
                else:
                    self.getAllArctisDevices()
                    time.sleep(1)
                    attempts = attempts - 1
        return None

    def setDeviceAsActive(self, device:ArctisDevice):
        self.getAllArctisDevices()
        indexOfSelectedDevice = [i for i, n in enumerate(self.arctisDevices) if
                                 n.idVendor == device.idVendor and n.idProduct == device.idProduct]
        if indexOfSelectedDevice:
            self.currentDevice = device
            self.currentDevice.isActive = True
            self.arctisDevices[indexOfSelectedDevice[0]] = self.currentDevice
            self.onSelectedDeviceChanged.emit(self.currentDevice)
            arctisSonarGUI.log(LogLevel.Info, f"Selected Device Changed to {device.name}")
            return True
        return False

    def updateLastDevice(self, device:ArctisDevice):
        if self.checkDeviceConnected(device.idVendor, device.idProduct):
            arctisSonarGUI.updateApplicationSettings("Device Details", "deviceIDVendor", device.idVendor)
            arctisSonarGUI.updateApplicationSettings("Device Details", "deviceIDProduct", device.idProduct)

    def kill(self):
        arctisSonarGUI.log(LogLevel.Info, 'Cleanup on shutdown')
        defaultSink = arctisSonarGUI.retrieveApplicationSetting("Sink Details", "defaultSink", None)
        arctisSonarGUI.log(LogLevel.Info, f'Setting default sink to {defaultSink}')
        sink_list = pulse.sink_list()
        for sink in sink_list:
            if defaultSink is not None and sink.name == defaultSink:
                os.system(f"pactl set-default-sink {sink.name}")
            else:
                os.system(f"pactl set-default-sink {sink.name}")

        self.destroyCreatedVirtualSinks()

        if self.originalSink is not None:
            os.system(f'pactl set-default-sink {self.originalSink}')

        self.originalSink = None

    def run(self):
        self.chatVolumeLevel = 100
        self.gameVolumeLevel = 100

        while not self.quitEvent.is_set():
            try:
                if self.isHeadsetControlInstalled:
                    stdout = os.popen("headsetcontrol -m -o json").readlines()
                    headsetControlOutput = "\n".join(stdout)
                    headsetControlOutput = json.loads(headsetControlOutput)

                    if self.currentDevice is not None:
                        indexOfConnectedDevice = [i for i in headsetControlOutput["devices"] if
                                                  int(i["id_vendor"], 16) == self.currentDevice.idVendor and int(i["id_product"],
                                                                                                    16) == self.currentDevice.idProduct]
                        if indexOfConnectedDevice:
                            if not self.currentDevice.isActive:
                                self.setDeviceAsActive(self.currentDevice)
                            device = indexOfConnectedDevice[0]
                            level = device["chatmix"]
                            level = int(level)

                            tempGameLevel = 100 - ((level - 64) / 64 * 100)
                            tempChatLevel = 100 - (64 - level) / 64 * 100

                            if tempChatLevel < 0:
                                tempChatLevel = 0
                            if tempChatLevel > 100:
                                tempChatLevel = 100

                            if tempGameLevel < 0:
                                tempGameLevel = 0
                            if tempGameLevel > 100:
                                tempGameLevel = 100

                            tempChatLevel = int(tempChatLevel)
                            tempGameLevel = int(tempGameLevel)

                            if tempGameLevel != self.gameVolumeLevel or tempChatLevel != self.chatVolumeLevel:

                                os.system(f'pactl set-sink-volume {self.arctisGameSinkName} {tempGameLevel}%')
                                os.system(f'pactl set-sink-volume {self.arctisChatSinkName} {tempChatLevel}%')

                                self.chatVolumeLevel = tempChatLevel
                                self.gameVolumeLevel = tempGameLevel
                                self.onMixerChanged.emit(tempChatLevel, tempGameLevel)
                    time.sleep(0.05)
                else:
                    raise Exception("Headset Control was not installed or is not working properly. 'headsetcontrol -m -o json' reported an error")

            except Exception as e:
                arctisSonarGUI.log(LogLevel.Exception, f"Error occured while reading from headsetcontrol: {e}")
                self.quit()
        arctisSonarGUI.log(LogLevel.Info, f"Arctis Sonar is done")

    def quit(self):
        self.quitEvent.set()
        self.kill()
        super().quit()

arctisSonarListener = ArctisSonarListenerThread()