from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Theme(QObject):
    onThemeChanged = pyqtSignal()
    def __init__(self,
                 name,
                 isDark,
                 primaryColour,
                 secondaryColour,
                 backgroundColour,
                 audioDeviceFrameColour,
                 seperatorColour,
                 activeColour,
                 hoverColour,
                 primaryIconColour,
                 pressedPrimaryIconColour,
                 activePrimaryIconColour,
                 primaryButtonColour,
                 pressedPrimaryButtonColour,
                 activePrimaryButtonColour,
                 disabledColour,
                 disabledTextColour,
                 primaryTextColour,
                 textAreaBackground,
                 secondaryTextColour,
                 headerBackground,
                 tableHeaderBackgroundColour,
                 tableDividerColour,
                 optionButtonBackground,
                 alternatingRowColor,
                 highlightingColour,
                 selectionTextColour,
                 extraQSS="", *args, **kwargs):
        super(Theme,self).__init__(*args, **kwargs)
        self.name = name
        self.isDark = isDark
        self.primaryColour = primaryColour
        self.secondaryColour = secondaryColour
        self.backgroundColour = backgroundColour
        self.audioDeviceFrameColour = audioDeviceFrameColour
        self.activeColour = activeColour
        self.hoverColour = hoverColour
        self.seperatorColour = seperatorColour
        self.primaryIconColour = primaryIconColour
        self.pressedPrimaryIconColour = pressedPrimaryIconColour
        self.activePrimaryIconColour = activePrimaryIconColour
        self.primaryButtonColour = primaryButtonColour
        self.pressedPrimaryButtonColour = pressedPrimaryButtonColour
        self.activePrimaryButtonColour = activePrimaryButtonColour
        self.disabledColour = disabledColour
        self.disabledTextColour = disabledTextColour
        self.primaryTextColour = primaryTextColour
        self.secondaryTextColour = secondaryTextColour
        self.textAreaBackground = textAreaBackground
        self.alternatingRowColor = alternatingRowColor
        self.headerBackground = headerBackground
        self.optionButtonBackground = optionButtonBackground
        self.tableHeaderBackgroundColour = tableHeaderBackgroundColour
        self.tableDividerColour = tableDividerColour
        self.highlightingColour = highlightingColour
        self.selectionTextColour = selectionTextColour
        self.iconSize = QSize(30, 30)
        self.extraQSS = extraQSS

        self.palette = QPalette()
        self.createPalette()

    def createPalette(self):

        self.palette.setColor(QPalette.ColorRole.Window, QColor(self.backgroundColour))
        self.palette.setColor(QPalette.ColorRole.Dark, QColor(self.backgroundColour))
        self.palette.setColor(QPalette.ColorRole.WindowText, QColor(self.primaryTextColour))
        self.palette.setColor(QPalette.ColorRole.Base, QColor(self.textAreaBackground))
        self.palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.alternatingRowColor))
        self.palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self.textAreaBackground))
        self.palette.setColor(QPalette.ColorRole.ToolTipText, QColor(self.primaryTextColour))

        self.palette.setColor(QPalette.ColorRole.Highlight, QColor(self.highlightingColour))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.selectionTextColour))

        self.palette.setColor(QPalette.ColorRole.Button, QColor(self.primaryButtonColour))
        self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.primaryTextColour))

        self.palette.setColor(QPalette.ColorRole.Button, QColor(self.disabledColour))
        self.palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.disabledTextColour))

        self.palette.setColor(QPalette.ColorRole.Text, QColor(self.primaryTextColour))
        self.palette.setColor(QPalette.ColorRole.Base, QColor(self.textAreaBackground))
        self.palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(self.disabledTextColour))
        self.palette.setColor(QPalette.ColorRole.Highlight, QColor(self.highlightingColour))
        self.palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.selectionTextColour))

    def changeTheme(self, newTheme):
        self.name = newTheme.name
        self.isDark = newTheme.isDark
        self.primaryColour = newTheme.primaryColour
        self.secondaryColour = newTheme.secondaryColour
        self.backgroundColour = newTheme.backgroundColour
        self.seperatorColour = newTheme.seperatorColour
        self.activeColour = newTheme.activeColour
        self.hoverColour = newTheme.hoverColour
        self.primaryIconColour = newTheme.primaryIconColour
        self.pressedPrimaryIconColour = newTheme.pressedPrimaryIconColour
        self.activePrimaryIconColour = newTheme.activePrimaryIconColour
        self.primaryButtonColour = newTheme.primaryButtonColour
        self.pressedPrimaryButtonColour = newTheme.pressedPrimaryButtonColour
        self.activePrimaryButtonColour = newTheme.activePrimaryButtonColour
        self.disabledColour = newTheme.disabledColour
        self.disabledTextColour = newTheme.disabledTextColour
        self.primaryTextColour = newTheme.primaryTextColour
        self.secondaryTextColour = newTheme.secondaryTextColour
        self.textAreaBackground = newTheme.textAreaBackground
        self.alternatingRowColor = newTheme.alternatingRowColor
        self.headerBackground = newTheme.headerBackground
        self.optionButtonBackground = newTheme.optionButtonBackground
        self.tableHeaderBackgroundColour = newTheme.tableHeaderBackgroundColour
        self.tableDividerColour = newTheme.tableDividerColour
        self.highlightingColour = newTheme.highlightingColour
        self.selectionTextColour = newTheme.selectionTextColour
        self.extraQSS = newTheme.extraQSS
        self.createPalette()
        self.onThemeChanged.emit()

steelseries_stealth = Theme(
    name="SteelSeries Stealth",
    isDark=True,
    audioDeviceFrameColour = "#2D363E",
    primaryColour="#2D363E",
    secondaryColour="#1B2228",
    backgroundColour="#16191E",
    seperatorColour="#38434D",
    activeColour="#FB4A00",
    hoverColour="#37434D",
    primaryIconColour="#8D96AA",
    pressedPrimaryIconColour="#FFFFFF",
    activePrimaryIconColour="#8D96AA",
    primaryButtonColour="#2D363E",
    pressedPrimaryButtonColour="#1E252A",
    activePrimaryButtonColour="#3E4B56",
    disabledColour="#252525",
    disabledTextColour="#555E6B",
    primaryTextColour="#FFFFFF",
    secondaryTextColour="#8D96AA",
    textAreaBackground="#0D1113",
    headerBackground="#1B2228",
    tableHeaderBackgroundColour="#1B2228",
    tableDividerColour="#2D363E",
    optionButtonBackground="#2D363E",
    alternatingRowColor="#161C20",
    highlightingColour="#8D96AA",
    selectionTextColour="#FFFFFF",
    extraQSS="""
    
    QScrollBar {
        background: #2C2C2C;
        border-radius: 5px;
    }

    QScrollBar:horizontal {
        height: 15px;
    }

    QScrollBar:vertical {
        width: 10px;
    }

    QScrollBar::handle {
        background: #464646;
        border-radius: 5px;
    }

    QScrollBar::handle:horizontal {
        height: 5px;
        min-width: 10px;
        border-radius: 5px;
    }

    QScrollBar::handle:vertical {
        width: 5px;
        min-height: 10px;
        border-radius: 5px;
    }

    QScrollBar::add-line {
        border: none;
        background: none;
    }

    QScrollBar::sub-line {
        border: none;
        background: none;
    }
    """
)

themeList = [steelseries_stealth]

currentTheme = themeList[0]