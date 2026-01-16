from arctis_sonar_globals import arctisSonarGUI, arctisSonarListener, LogLevel
from ui.ui import *
import usb.core

if __name__ == "__main__":
    enableArctisGUI = arctisSonarGUI.returnBoolSetting("Application Settings", "enableSonar", True)
    if enableArctisGUI:
        arctisSonarListener.start(QThread.Priority.IdlePriority)
    initialiseUI()
    arctisSonarGUI.log(LogLevel.Info, f"Closing ArctisSonar GUI")
    arctisSonarListener.quit()
    arctisSonarListener.wait(5)
    arctisSonarGUI.log(LogLevel.Info, f"Closed ArctisSonar GUI")

