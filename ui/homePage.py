from PyQt6.QtWidgets import *

import ui.globalComponents as globalComponents
from ui.assets.themes import *
from arctis_sonar_globals import arctisSonarGUI, arctisSonarListener, ArctisDevice, LogLevel


class HomePage(QWidget):
    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

        self.gameAudioDeviceFrame = globalComponents.AudioDeviceFrame(
            name="Game",
            icon=globalComponents.arctisSonarIcons.gameIcon,
            colour="#04C5A8",
            volumeRangeColours={0: "#04C5A8"},
            volumeLevel=100
        )
        self.chatAudioDeviceFrame = globalComponents.AudioDeviceFrame(
            name="Chat",
            icon=globalComponents.arctisSonarIcons.chatIcon,
            colour="#2791CE",
            volumeRangeColours={0: "#2791CE"},
            volumeLevel = 100
        )

        self.currentAudioDeviceLabel = globalComponents.ColorLabel(
            text="Select a device",
            textColor=currentTheme.disabledTextColour,
            font=globalComponents.arctisSonarFonts.extraBold
        )

        virtualAudioDevicesLayout = QHBoxLayout()
        virtualAudioDevicesLayout.addWidget(self.gameAudioDeviceFrame)
        virtualAudioDevicesLayout.addWidget(self.chatAudioDeviceFrame)
        virtualAudioDevicesLayout.addStretch()
        virtualAudioDevicesLayout.setSpacing(35)

        homePageLayout = QVBoxLayout()
        homePageLayout.addWidget(self.currentAudioDeviceLabel)
        homePageLayout.addLayout(virtualAudioDevicesLayout, stretch=1)
        homePageLayout.addStretch()
        homePageLayout.setSpacing(50)

        self.setLayout(homePageLayout)

        arctisSonarListener.onMixerChanged.connect(self.updateMixers)
        arctisSonarListener.onSelectedDeviceChanged.connect(self.onAudioDeviceSelected)

        lastDevice = arctisSonarListener.returnCurrentDevice()
        self.onAudioDeviceSelected(lastDevice)


    def onAudioDeviceSelected(self, device:ArctisDevice):
        if device is not None:
            self.currentAudioDeviceLabel.updateText(device.name, globalComponents.returnColourCode(currentTheme.activeColour) if device.isActive else globalComponents.returnColourCode(currentTheme.disabledColour))
        else:
            self.currentAudioDeviceLabel.updateText("Select a device", globalComponents.returnColourCode(
                currentTheme.disabledColour))

    def updateMixers(self, chatLevel, gameLevel):
        self.gameAudioDeviceFrame.setVolume(gameLevel)
        self.chatAudioDeviceFrame.setVolume(chatLevel)
        logChatMix = arctisSonarGUI.returnBoolSetting("Application Settings", "logChatMix", False)
        if logChatMix:
            arctisSonarGUI.log(LogLevel.Debug, f"Chat Level = {chatLevel}. Game Level = {gameLevel}")
        # print(gameLevel, chatLevel)