import datetime
import functools
import logging

from PyQt6.QtWidgets import *
from superqt import QToggleSwitch

import ui.globalComponents as globalComponents
from ui.assets.themes import *
from arctis_sonar_globals import arctisSonarGUI, arctisSonarListener, ArctisDevice


class LogCallbackHandler(logging.Handler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def emit(self, record):
        # record.getMessage() gets the final string
        try:
            self.callback(self.format(record))
        except:
            pass

class SettingsPage(QWidget):
    def __init__(self, *args, **kwargs):
        super(SettingsPage, self).__init__(*args, **kwargs)

        generalSettingsLabel = globalComponents.ColorLabel(
            text = "General Settings",
            font=globalComponents.arctisSonarFonts.header2,
            textColor="#666666"
        )

        self.buildVersionLabel = QLabel(arctisSonarGUI.buildVersion)

        self.enableArctisGUISwitch = QToggleSwitch()
        self.enableArctisGUISwitch._set_switchWidth(30)
        self.enableArctisGUISwitch._set_handleSize(15)
        self.enableArctisGUISwitch._set_switchHeight(15)
        enableArctisGUI = arctisSonarGUI.returnBoolSetting("Application Settings", "enableSonar", True)
        self.enableArctisGUISwitch.setChecked(enableArctisGUI)
        self.enableArctisGUISwitch.toggled.connect(self.updateEnableArctisGUISwitch)

        self.changeDeviceOnStartupSwitch = QToggleSwitch()
        self.changeDeviceOnStartupSwitch._set_switchWidth(30)
        self.changeDeviceOnStartupSwitch._set_handleSize(15)
        self.changeDeviceOnStartupSwitch._set_switchHeight(15)

        self.checkHeadsetControlInstalledButton = globalComponents.RoundedButton(
            label="Check Headset Control Installed",
        )
        self.checkHeadsetControlInstalledButton.clicked.connect(self.checkHeadsetControlInstalled)

        changeDeviceOnStartup = arctisSonarGUI.returnBoolSetting("Sink Details", "changeAudioDeviceOnStartup", True)
        self.changeDeviceOnStartupSwitch.setChecked(changeDeviceOnStartup)
        self.changeDeviceOnStartupSwitch.toggled.connect(self.updateChangeDeviceOnStartupSwitch)

        generalSettingsFormLayout = QFormLayout()
        generalSettingsFormLayout.addRow(globalComponents.BoldLabel("Build Version"), self.buildVersionLabel)
        generalSettingsFormLayout.addRow(globalComponents.BoldLabel("Enable Arctis GUI"), self.enableArctisGUISwitch)
        generalSettingsFormLayout.addRow(globalComponents.BoldLabel("Change Audio Device On Startup"), self.changeDeviceOnStartupSwitch)
        generalSettingsFormLayout.addRow(globalComponents.BoldLabel("Confirm Headset Control Installed"), self.checkHeadsetControlInstalledButton)

        self.devicesStackedWidget = QStackedWidget()
        self.createDevicesStackedWidget()

        devicesLabel = globalComponents.ColorLabel(
            text="Devices",
            font=globalComponents.arctisSonarFonts.header2,
            textColor="#666666"
        )

        logLabel = globalComponents.ColorLabel(
            text="Log",
            font=globalComponents.arctisSonarFonts.header2,
            textColor="#666666"
        )

        self.logs = []

        self.logPlainText = QLabel()
        self.logPlainText.setEnabled(True)
        self.logPlainText.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.logPlainText.setWordWrap(True)

        self.logHistoryAutoScrollCheck = QToggleSwitch()
        self.logHistoryAutoScrollCheck._set_switchWidth(30)
        self.logHistoryAutoScrollCheck._set_handleSize(15)
        self.logHistoryAutoScrollCheck._set_switchHeight(15)
        self.logHistoryAutoScrollCheck.setChecked(True)

        self.logChatMixChangesCheck = QToggleSwitch()
        self.logChatMixChangesCheck._set_switchWidth(30)
        self.logChatMixChangesCheck._set_handleSize(15)
        self.logChatMixChangesCheck._set_switchHeight(15)
        logChatMix = arctisSonarGUI.returnBoolSetting("Application Settings", "logChatMix", False)
        self.logChatMixChangesCheck.setChecked(logChatMix)
        self.logChatMixChangesCheck.toggled.connect(self.onLogChatMixToggled)

        self.logScrollArea = QScrollArea(self)
        self.logScrollArea.setWidget(self.logPlainText)
        self.logScrollArea.setWidgetResizable(True)
        self.logScrollArea.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.logScrollArea.setContentsMargins(0, 0, 0, 0)
        self.logScrollArea.setFixedHeight(300)

        logAutoScrollLayout = QFormLayout()
        logAutoScrollLayout.addRow(globalComponents.BoldLabel("Autoscroll Log"), self.logHistoryAutoScrollCheck)
        logAutoScrollLayout.addRow(globalComponents.BoldLabel("Log Chatmix"), self.logChatMixChangesCheck)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(generalSettingsLabel)
        mainLayout.addLayout(generalSettingsFormLayout)
        mainLayout.addWidget(globalComponents.DividerLine())
        mainLayout.addWidget(devicesLabel)
        mainLayout.addWidget(self.devicesStackedWidget)
        mainLayout.addWidget(globalComponents.DividerLine())
        mainLayout.addWidget(logLabel)
        mainLayout.addLayout(logAutoScrollLayout)
        mainLayout.addWidget(self.logScrollArea)
        mainLayout.addStretch()

        mainLayout.setSpacing(25)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)

        scrollWidget = QScrollArea()
        scrollWidget.setWidgetResizable(True)
        scrollWidget.setWidget(mainWidget)
        scrollWidget.setStyleSheet("background-color: transparent;")

        arctisSonarListener.onAvailableDevicesChanged.connect(self.createDevicesStackedWidget)
        arctisSonarListener.onSelectedDeviceChanged.connect(self.createDevicesStackedWidget)

        layout = QVBoxLayout()
        layout.addWidget(scrollWidget, stretch = 1)
        self.setLayout(layout)

        self.logCallback = LogCallbackHandler(self.addLog)

        arctisSonarGUI.addHandlerToLogger(self.logCallback)

    def checkHeadsetControlInstalled(self):
        arctisSonarListener.checkHeadsetControlInstalled()
        if not arctisSonarListener.isHeadsetControlInstalled:
            globalComponents.CustomDialog(
                title="HeadsetControl is not installed",
                description="HeadsetControl is not installed or is not working properly. Install HeadsetControl on your system"
            ).exec()

    def createDevicesStackedWidget(self):
        if self.devicesStackedWidget.currentWidget() is not None:
            self.devicesStackedWidget.removeWidget(self.devicesStackedWidget.currentWidget())

        layout = QVBoxLayout()
        for device in arctisSonarListener.arctisDevices:
            deviceButton = globalComponents.HeadphoneButton(device)
            deviceButton.setFixedHeight(90)
            deviceButton.clicked.connect(functools.partial(self.onAudioDeviceSelected, device))
            layout.addWidget(deviceButton)
        layout.addStretch(1)
        layout.setSpacing(12)

        widget = QWidget()
        widget.setLayout(layout)

        self.devicesStackedWidget.addWidget(widget)

    def updateEnableArctisGUISwitch(self):
        enableArctisGUI = self.enableArctisGUISwitch.isChecked()
        arctisSonarGUI.updateApplicationSettings("Application Settings", "enableSonar", enableArctisGUI)

        if enableArctisGUI:
            arctisSonarListener.start(QThread.Priority.IdlePriority)
        else:
            arctisSonarListener.quit()
            arctisSonarListener.wait()

    def updateChangeDeviceOnStartupSwitch(self):
        changeDeviceOnStartup = self.changeDeviceOnStartupSwitch.isChecked()
        arctisSonarGUI.updateApplicationSettings("Sink Details", "changeAudioDeviceOnStartup", changeDeviceOnStartup)

    def onAudioDeviceSelected(self, device:ArctisDevice):
        if device is not None:
            rc = arctisSonarListener.setDeviceAsActive(device)
            if rc:
                arctisSonarListener.updateLastDevice(device)
            else:

                globalComponents.CustomDialog(
                    title="Unable to set device as selected",
                    description=f"Unable to set device as selected. This device is not currently connected.",
                )

    def onLogChatMixToggled(self):
        logChatMix = self.logChatMixChangesCheck.isChecked()
        arctisSonarGUI.updateApplicationSettings("Application Settings", "logChatMix", logChatMix)

    def addLog(self,log):
        self.logs.append([log,datetime.datetime.now()])
        text = ""
        for i in self.logs:
            text += f"<div><a style='color:{globalComponents.currentTheme.disabledTextColour};'>{i[1]}</a> :: {i[0]}</div><hr/>\n"
        self.logPlainText.setText(text)
        self.logPlainText.setAlignment(Qt.AlignmentFlag.AlignTop)

        if self.logHistoryAutoScrollCheck.isChecked():
            self.logScrollArea.verticalScrollBar().setValue(self.logScrollArea.verticalScrollBar().maximum())