import asyncio
import functools
import sys
import webbrowser

from PyQt6.QtWidgets import *
from PyQt6.QtSvg import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

import ui.globalComponents as globalComponents
from ui.assets.themes import *
from arctis_sonar_globals import arctisSonarGUI, arctisSonarListener
from ui.homePage import HomePage
from ui.settingsPage import SettingsPage

class SideBar(QWidget):
    onButtonClicked = pyqtSignal(str)
    def __init__(self, *args, **kwargs):
        super(SideBar, self).__init__(*args, **kwargs)

        self.homeButton = globalComponents.SideBarButton(
            name = "Home",
            svg = globalComponents.arctisSonarIcons.homeIcon,
            svgColor = "#8D96AA",
            borderRadius = 22,
            backgroundColor="#1B1E22"
        )
        self.homeButton.setFixedSize(QSize(120, 130))
        self.homeButton.svgWidget.setFixedSize(QSize(60,60))
        self.homeButton.clicked.connect(lambda : self.onButtonClicked.emit("Home"))

        self.settingsButton = globalComponents.SideBarButton(
            name="Settings",
            svg=globalComponents.arctisSonarIcons.settingsIcon,
            svgColor="#8D96AA",
            borderRadius = 22,
            backgroundColor="#1B1E22"
        )
        self.settingsButton.setFixedSize(QSize(120, 130))
        self.settingsButton.svgWidget.setFixedSize(QSize(60, 60))
        self.settingsButton.clicked.connect(lambda : self.onButtonClicked.emit("Settings"))

        self.helpButton = globalComponents.SideBarButton(
            name="Help",
            svg=globalComponents.arctisSonarIcons.helpIcon,
            svgColor="#8D96AA",
            borderRadius=22,
            backgroundColor="#1B1E22"
        )
        self.helpButton.setFixedSize(QSize(120, 130))
        self.helpButton.svgWidget.setFixedSize(QSize(60, 60))
        self.helpButton.clicked.connect(lambda: self.onButtonClicked.emit("Help"))

        layout = QVBoxLayout()
        layout.addWidget(self.homeButton)
        layout.addWidget(self.settingsButton)
        layout.addStretch()
        layout.addWidget(self.helpButton)
        layout.setSpacing(30)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle(arctisSonarGUI.applicationName)

        self.isQuitting = False

        trayMenu = QMenu()
        openAppAction = QAction("Open ArctisSonar GUI",self)
        openAppAction.triggered.connect(self.showWindow)

        trayMenu.addAction(openAppAction)

        quitAppAction = QAction("Quit",self)
        quitAppAction.triggered.connect(self.quitApplication)
        trayMenu.addAction(quitAppAction)

        tray = QSystemTrayIcon(QIcon(globalComponents.arctisSonarIcons.appIconImage), parent=self)
        tray.setContextMenu(trayMenu)
        tray.show()

        tray.activated.connect(self.on_tray_icon_activated)

        currentTheme.onThemeChanged.emit()

        self.showChangeLogTimer = QTimer(self)
        self.showChangeLogTimer.setSingleShot(True)
        self.showChangeLogTimer.timeout.connect(self.showChangeLog)

        self.checkHeadsetControlInstalledTimer = QTimer(self)
        self.checkHeadsetControlInstalledTimer.setSingleShot(True)
        self.checkHeadsetControlInstalledTimer.setInterval(1000)
        self.checkHeadsetControlInstalledTimer.timeout.connect(self.checkHeadsetControlInstalled)
        self.checkHeadsetControlInstalledTimer.start()

        lastRunningVersion = arctisSonarGUI.retrieveApplicationSetting("Application Info", "lastRunningVersion", None)
        if lastRunningVersion != arctisSonarGUI.buildVersion:
            arctisSonarGUI.updateApplicationSettings("Application Info", "lastRunningVersion",arctisSonarGUI.buildVersion)
            self.showChangeLogTimer.start(1000)

        self.setWindowFlags((self.windowFlags() & ~Qt.WindowType.WindowFullscreenButtonHint & ~Qt.WindowType.WindowMaximizeButtonHint) | Qt.WindowType.CustomizeWindowHint)

        self.sideBar = SideBar()
        self.sideBar.onButtonClicked.connect(self.changePage)

        applicationNameLabel = QLabel(arctisSonarGUI.applicationName)
        applicationNameLabel.setFont(globalComponents.arctisSonarFonts.header2)

        self.homePageWidget = HomePage()
        self.settingsPageWidget = SettingsPage()

        self.currentPageStackedWidget = QStackedWidget()
        self.currentPageWidget = self.homePageWidget
        self.currentPageStackedWidget.addWidget(self.homePageWidget)

        contentLayout = QVBoxLayout()
        contentLayout.setSpacing(30)
        contentLayout.addWidget(applicationNameLabel)
        contentLayout.addWidget(self.currentPageStackedWidget, stretch=1)
        contentLayout.setContentsMargins(25,25,25,25)

        contentWidgetFramedWidget = globalComponents.FramedWidget(
            layout=contentLayout,
        )

        layout = QHBoxLayout()
        layout.addWidget(self.sideBar, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(contentWidgetFramedWidget, stretch=1)
        layout.setContentsMargins(0,0,0,0)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        mainWidget.setContentsMargins(10,10,10,10)

        self.setCentralWidget(mainWidget)

        self.setMaximumWidth(self.sizeHint().width())
        self.setMinimumHeight(700)

    def showChangeLog(self):
        globalComponents.ChangeLogDialog().exec()

    def checkHeadsetControlInstalled(self):
        arctisSonarListener.checkHeadsetControlInstalled()
        if not arctisSonarListener.isHeadsetControlInstalled:
            globalComponents.CustomDialog(
                title="HeadsetControl is not installed",
                description="HeadsetControl is not installed or is not working properly. Install HeadsetControl on your system"
            ).exec()

    def changePage(self, pageName):
        try:
            if pageName == "Home":
                if self.currentPageWidget != self.homePageWidget:
                    self.currentPageStackedWidget.removeWidget(self.currentPageWidget)
                    self.currentPageWidget = self.homePageWidget
                    self.currentPageStackedWidget.addWidget(self.currentPageWidget)

            elif pageName == "Settings":
                if self.currentPageWidget != self.settingsPageWidget:
                    self.currentPageStackedWidget.removeWidget(self.currentPageWidget)
                    self.currentPageWidget = self.settingsPageWidget
                    self.currentPageStackedWidget.addWidget(self.currentPageWidget)

            elif pageName == "Help":
                print("opening help")
                webbrowser.open("https://github.com/Michael-Adu/ArctisSonarGUI", new = 0, autoraise = True)
        
        except Exception as e:
            pass

    def closeEvent(self, event):
        if self.isQuitting:
            super().closeEvent(event)
        else:
            self.showMinimized()
            event.ignore()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showWindow()
        elif reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showWindow()

    def quitApplication(self):
        self.isQuitting = True
        self.close()

    def showWindow(self):
        self.show()
        self.activateWindow()

def initialiseUI():
    global mainUI
    app = QApplication(sys.argv)
    currentThemeName = arctisSonarGUI.retrieveApplicationSetting("UI", "theme", "Dark Theme")
    indexOfTheme = [i for i, theme in enumerate(themeList) if theme.name == currentThemeName]
    if indexOfTheme:
        indexOfTheme = indexOfTheme[0]
    else:
        indexOfTheme = 0

    currentTheme.changeTheme(themeList[indexOfTheme])
    arctisSonarGUI.updateApplicationSettings("UI", "theme", themeList[indexOfTheme].name)
    app.setPalette(currentTheme.palette)

    app.setStyleSheet(currentTheme.extraQSS)
    globalComponents.arctisSonarFonts = globalComponents.ArctisSonarFonts()
    globalComponents.arctisSonarIcons = globalComponents.ArctisSonarIcons()

    app.setFont(globalComponents.arctisSonarFonts.normal)

    QApplication.instance().setWindowIcon(QIcon(globalComponents.arctisSonarIcons.appIcon))
    mainUI = MainWindow()
    mainUI.show()

    app_close_event = asyncio.Event()
    app.aboutToQuit.connect(app_close_event.set)

    QApplication.setStyle(QStyleFactory.create("Fusion"))

    return app.exec()