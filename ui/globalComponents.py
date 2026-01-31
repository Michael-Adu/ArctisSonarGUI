import os

import markdown
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtSvg import *
from superqt import QDoubleSlider
import xml.etree.ElementTree as ET
import arctis_sonar_globals
from arctis_sonar_globals import ArctisDevice
from ui.assets.themes import *

class ArctisSonarFonts:
    def __init__(self):
        applicationPath = arctis_sonar_globals.arctisSonarGUI.returnApplicationPath()
        appFontSize = arctis_sonar_globals.arctisSonarGUI.retrieveApplicationSetting("UI", "fontSize", 10)
        sizeIncrease = int(appFontSize) - 10
        if sizeIncrease < 0:
            sizeIncrease = 0

        self.fontName = "Onest"
        QFontDatabase.addApplicationFont(applicationPath + "ui/assets/fonts/Onest-VariableFont_wght.ttf")

        self.normal = QFont(self.fontName, 10 + sizeIncrease)
        self.normalSmall = QFont(self.fontName, 8 + sizeIncrease)
        self.header1 = QFont(self.fontName, 36 + sizeIncrease, 700)
        self.header2 = QFont(self.fontName, 24 + sizeIncrease, 700)
        self.header3 = QFont(self.fontName, 14 + sizeIncrease, 700)
        self.extraBold = QFont(self.fontName, 11 + sizeIncrease, 900)
        self.normalBold = QFont(self.fontName, 10 + sizeIncrease, 1800)
        self.semiBold = QFont(self.fontName, 11 + sizeIncrease, 600)
        self.largeBold = QFont(self.fontName, 12 + sizeIncrease, 700)
        self.normalSmallBold = QFont(self.fontName, 8 + sizeIncrease, 600)
        self.normalItalics = QFont(self.fontName, 11 + sizeIncrease, -1, True)
        self.normalBoldItalics = QFont(self.fontName, 11 + sizeIncrease, 700, True)

arctisSonarFonts:ArctisSonarFonts|None = None ## initialized in ui.py

class ArctisSonarIcons:
    def __init__(self):
        applicationPath = arctis_sonar_globals.arctisSonarGUI.returnApplicationPath()
        self.appIcon = applicationPath + "ui/assets/svgs/appIcon.svg"
        self.appIconImage = applicationPath + "ui/assets/appIcon.png"
        self.homeIcon = applicationPath + "ui/assets/svgs/home.svg"
        self.settingsIcon = applicationPath + "ui/assets/svgs/settings.svg"
        self.gameIcon = applicationPath + "ui/assets/svgs/game.svg"
        self.chatIcon = applicationPath + "ui/assets/svgs/chat.svg"
        self.headphoneIcon = applicationPath + "ui/assets/svgs/headphone.svg"
        self.helpIcon = applicationPath + "ui/assets/svgs/help.svg"

arctisSonarIcons:ArctisSonarIcons|None = None ## initialized in ui.py

class CustomSvgWidget(QWidget):
    """
    Custom SVG widget to display SVG files while keeping the aspect ratio and resolution.
    """
    def __init__(self, svg_file, color: str, *args, **kwargs):
        """
        Initialize the widget with the provided SVG file and color.

        :param svg_file: The path to the SVG file.
        :param color: The color to fill the SVG with.
       """
        super(CustomSvgWidget, self).__init__(*args, **kwargs)
        self.svg_file = svg_file
        self.svg_content = ""
        self.renderer = QSvgRenderer()
        self.fill_color = color
        self.svgOriginalSize = QSize(0, 0)
        self.load_svg_file(self.svg_file, self.fill_color)

    def load_svg_file(self, svg_file, color):
        """
        Load the SVG file and update the renderer.

        :param svg_file: The path to the SVG file.
        :param color: The color to fill the SVG with.
        """
        self.fill_color = color
        self.svg_file = svg_file
        self.svg_content = self.change_svg(self.svg_file, self.fill_color, self.fill_color)
        self.update_renderer()

    def setFixedSize(self, a0: QSize, strict=False):
        """
        Set the fixed size of the widget based on the provided size.

        :param a0: The new fixed size as a QSize.
        :param strict: If True, the width and height will be set strictly, otherwise, the aspect ratio will be maintained.
        """
        widthToHeightRatio = self.svgOriginalSize.width() / self.svgOriginalSize.height()
        newHeight = a0.height()
        if strict:
            newWidth = a0.width()
        else:
            newWidth = int(newHeight * widthToHeightRatio)
        newSize = QSize(
            newWidth,
            newHeight
        )
        super().setFixedSize(newSize)

    def setMinimumSize(self, a0: QSize, strict=False):
        """
        Set the fixed size of the widget based on the provided size.

        :param a0: The new fixed size as a QSize.
        :param strict: If True, the width and height will be set strictly, otherwise, the aspect ratio will be maintained.
        """
        widthToHeightRatio = self.svgOriginalSize.width() / self.svgOriginalSize.height()
        newHeight = a0.height()
        if strict:
            newWidth = a0.width()
        else:
            newWidth = int(newHeight * widthToHeightRatio)
        newSize = QSize(
            newWidth,
            newHeight
        )
        super().setMinimumSize(newSize)

    def setMaximumSize(self, a0: QSize, strict=False):
        """
        Set the fixed size of the widget based on the provided size.

        :param a0: The new fixed size as a QSize.
        :param strict: If True, the width and height will be set strictly, otherwise, the aspect ratio will be maintained.
        """
        widthToHeightRatio = self.svgOriginalSize.width() / self.svgOriginalSize.height()
        newHeight = a0.height()
        if strict:
            newWidth = a0.width()
        else:
            newWidth = int(newHeight * widthToHeightRatio)
        newSize = QSize(
            newWidth,
            newHeight
        )
        super().setMaximumSize(newSize)

    def updateColor(self, color: str):
        """
        Update the fill color of the SVG and update the renderer.
        :param color: Color in either hexadecimal or as a common string
        :return:
        """
        self.fill_color = color
        self.svg_content = self.change_svg(self.svg_file, self.fill_color, self.fill_color)
        self.update_renderer()

    def update_renderer(self):
        """
        Update the SVG renderer with the new SVG content and update the widget.
        """
        self.renderer.load(QByteArray(self.svg_content.encode('utf-8')))
        self.update()

    def change_svg(self, input_file, new_fill_color, new_stroke_color):
        """
        Change the SVG file with a new fill and stroke color.
        Used internally when the class is initialized.
        :param input_file: Path to the SVG file
        :param new_fill_color: Fill Color
        :param new_stroke_color: Stroke Color
        :return:
        """

        # Parse the SVG file
        tree = ET.parse(input_file)
        root = tree.getroot()

        width = int(root.attrib.get("width", "100"))
        height = int(root.attrib.get("height", "100"))
        self.svgOriginalSize = QSize(width, height)
        # Define namespaces
        namespaces = {'svg': 'http://www.w3.org/2000/svg'}

        # Iterate through all elements that can have fill and stroke attributes
        for elem in root.findall(".//*[@fill]", namespaces):
            fill = elem.get('fill')
            if fill and fill.lower() != 'none' and fill.lower() != 'transparent':
                elem.set('fill', new_fill_color)

        for elem in root.findall(".//*[@stroke]", namespaces):
            stroke = elem.get('stroke')
            if stroke and stroke.lower() != 'none':
                elem.set('stroke', new_stroke_color)

        # Convert the modified SVG tree to a string
        svg_string = ET.tostring(root, encoding='unicode')
        return svg_string

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.renderer.isValid():
            return
        self.renderer.render(painter)

class DividerLine(QFrame):
    """
    A DividerLine widget with customizable orientation.
    """
    def __init__(self, orientation=Qt.Orientation.Horizontal,color="black", *args, **kwargs):
        super(DividerLine, self).__init__(*args, **kwargs)
        self.lineColor = returnColourCode(color)
        if orientation == Qt.Orientation.Vertical:
            shape = QFrame.Shape.VLine
        else:
            shape = QFrame.Shape.HLine
        self.setFrameShape(shape)
        self.setGeometry((QRect(1, 1, 1, 1)))

    def updateLineColor(self,color):
        self.lineColor = returnColourCode(color)
        self.update()

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setBrush(QColor(self.lineColor))
        painter.drawRect(self.rect())

class FramedWidget(QWidget):
    """
    A DividerLine widget with customizable orientation.
    """
    def __init__(self, widget:QWidget|None = None, layout = None, colour="#1C1E23", margin = 40, borderRadius = 35,  *args, **kwargs):
        super(FramedWidget, self).__init__(*args, **kwargs)
        self.widget = widget
        self.colour = colour
        self.borderRadius = borderRadius
        if widget is None:
            mainLayout = layout
        else:

            mainLayout = QVBoxLayout()
            mainLayout.addWidget(self.widget, stretch = 1)
            mainLayout.setContentsMargins(margin, margin, margin, margin)
        self.setLayout(mainLayout)

    def paintEvent(self, a0):
        painter = QPainter(self)
        background_color = QColor(returnColourCode(self.colour))
        painter.setBrush(QBrush(background_color))

        # Set the border color and thickness
        border_color = QColor("transparent")
        pen = QPen(border_color)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw the button rectangle with background and border
        painter.drawRoundedRect(self.rect(), self.borderRadius, self.borderRadius)

class ColorLabel(QLabel):
    """
    A label that can change its text color and can create a border. Useful for displaying status messages or other important information.
    """
    def __init__(self, text, font, textColor="black", borderColor="transparent", borderWidth=0, borderRadius=3, *args,
                 **kwargs):
        """
        Initialize the label with the given text, font, text color, border color, border width, and border radius.
        :param text: Text to be displayed in the label.
        :param font: Font to be used for displaying the text.
        :param textColor: Color of the text.
        :param borderColor: Border color.
        :param borderWidth: Border width
        :param borderRadius: Border radius.
        """
        super(ColorLabel, self).__init__(*args, **kwargs)
        self.originalTextColor = textColor
        self.currentTextColor = textColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.setText(text)
        self.setFont(font)
        if self.borderWidth > 0:
            self.setContentsMargins(5, 5, 5, 5)
        else:
            self.setContentsMargins(0, 0, 0, 0)

    def updateText(self, newText, color=None):
        """
        Update the text of the label with the given newText and, if provided, the new color.
        :param newText: Text to be displayed in the label.
        :param color: Color of the text.
        """
        if color != None:
            self.originalTextColor = color
            self.currentTextColor = color
        self.setText(newText)
        self.update()

    def setTextColor(self, color):
        """
        Update the color of the text in the label.
        :param color: Color of the text.
        """
        self.originalTextColor = returnColourCode(color)
        self.currentTextColor = returnColourCode(color)
        self.updateText(self.text())
        self.update()

    def setEnabled(self, enabled:bool):
        self.currentTextColor = returnColourCode(currentTheme.disabledTextColour if not enabled else self.originalTextColor)
        super().setEnabled(enabled)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.borderWidth != 0:
            pen = QPen(QColor(self.borderColor))
            pen.setWidth(self.borderWidth)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.drawRoundedRect(self.rect(), self.borderRadius, self.borderRadius)

        pen = QPen(QColor(self.currentTextColor))
        pen.setWidth(0)
        painter.setPen(pen)

        # Draw the HTML content
        # text_doc.drawContents(painter, QRectF(self.rect().x(),self.rect().y(), self.rect().width(),self.rect().height()))
        painter.drawText(self.rect(), self.alignment(), self.text())

class BoldLabel(QLabel):
    def __init__(self, labelString, font: ArctisSonarFonts|None = None, *args, **kwargs):
        super(BoldLabel, self).__init__(*args, **kwargs)
        self.setText(labelString)
        if font is None:
            self.setFont(arctisSonarFonts.normalBold)
        else:
            self.setFont(font)

class CustomProgressBar(QSlider):
    """
    A custom progress bar with different color ranges for different progress values.
    """
    def __init__(self, colorRanges={0: "red", 70: "yellow", 90: "green"}, *args, **kwargs):
        """
        Initialize the custom progress bar with the given color ranges.
        :param colorRanges: A dictionary mapping progress values to their respective colors.
        :param args:
        :param kwargs:
        """
        super(CustomProgressBar, self).__init__(*args, **kwargs)
        self.colorRanges: dict = colorRanges

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(10, 0)
        effect.setColor(QColor(currentTheme.optionButtonBackground))
        effect.setBlurRadius(1)

        self.setGraphicsEffect(effect)


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        newColor = QColor("blue")
        keyList = list(self.colorRanges.keys())
        rangeCount = len(keyList)
        for i in range(0, rangeCount):
            minColorRange = keyList[i]
            maxColorRange = self.maximum()
            if i + 1 < rangeCount:
                maxColorRange = keyList[i + 1]
            if minColorRange <= self.value() and self.value() <= maxColorRange:
                color = self.colorRanges[minColorRange]
                newColor = color

        progressColor = QColor(newColor)

        opt = QStyleOptionSlider()
        self.initStyleOption(opt)

        rect = self.contentsRect()


        # Handle Dimensions
        handle_w = 21
        handle_h = 73

        # --- 1. Draw Groove ---
        groove_width = 10
        # Vertical sliders need the groove to stay within the handle's travel range
        # We shrink the groove slightly so it doesn't peek out from behind the rounded handle
        groove_x = int(rect.center().x() - (groove_width / 2))
        groove_rect = QRect(groove_x, rect.top() + (handle_h // 2),
                            groove_width, rect.height() - handle_h)

        progress_height = int(rect.height() * (self.value() / 100))
        progress_rect = QRect(
            groove_x,
            rect.top() + (rect.height() - progress_height),
            groove_width,
            progress_height
        )


        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#22282A"))
        painter.drawRoundedRect(groove_rect, 5, 5)

        painter.setBrush(progressColor)
        painter.drawRoundedRect(progress_rect, 5, 5)

        # --- 2. Calculate Constrained Handle Position ---
        # Get the standard bounding box for the handle
        sr = self.style().subControlRect(
            QStyle.ComplexControl.CC_Slider,
            opt,
            QStyle.SubControl.SC_SliderHandle,
            self
        )

        # Calculate the Y position
        # We map the slider value to a range that accounts for the handle height
        available_height = rect.height() - handle_h

        # Calculate ratio (0.0 to 1.0) based on current value
        # Note: Vertical sliders are inverted (max is at top)
        if self.maximum() == self.minimum():
            ratio = 0
        else:
            ratio = (self.value() - self.minimum()) / (self.maximum() - self.minimum())

        # Calculate Y so that the handle is perfectly contained
        # At max value, handle_y = 0; at min value, handle_y = available_height
        handle_y = int((1 - ratio) * available_height)
        handle_x = int(rect.center().x() - (handle_w / 2))

        handle_rect = QRect(handle_x, handle_y, handle_w, handle_h)

        # --- 3. Draw Handle ---
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawRoundedRect(handle_rect, 10, 10)

        painter.end()

class SideBarButton(QAbstractButton):
    hovered = pyqtSignal(bool)
    """
    An icon button with an SVG and a customizable background color.
    """

    def __init__(self,
                 name,
                 svg,
                 svgColor=currentTheme.primaryIconColour,
                 backgroundColor=currentTheme.primaryButtonColour,
                 borderColor="transparent",
                 borderRadius=2,
                 borderWidth=0,
                 onClickColor=currentTheme.pressedPrimaryButtonColour,
                 *args, **kwargs):

        """
        Initialize the button with the given SVG, color, background color, border color, border width, border radius, and hover color.
        :param svg: The SVG file to be displayed inside the button.
        :param svgColor: The color of the SVG.
        :param backgroundColor: The background color of the button.
        :param borderColor: The border color of the button.
        :param borderRadius: The radius of the button's border.
        :param borderWidth: The width of the button's border.
        :param onClickColor: The color to apply when the button is clicked.
        """
        super(SideBarButton, self).__init__(*args, **kwargs)

        self.name = name
        self.svgFile = svg
        self.svgColor = svgColor
        self.backgroundColor = backgroundColor
        self.onClickColor = onClickColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.hoverColor = "black"
        try:
            self.hoverColor = darken_color(self.onClickColor)
        except Exception as e:
            print(e)

        self.currentBackgroundColor = backgroundColor
        self.currentBorderWidth = self.borderWidth
        self.currentBorderColor = self.borderColor
        self.paddingSize = 40

        self.svgWidget = CustomSvgWidget(self.svgFile, returnColourCode(self.svgColor))
        self.svgWidget.setFixedSize(QSize(60,60))
        self.label = ColorLabel(
            text=name,
            textColor=self.svgColor,
            font=arctisSonarFonts.semiBold
        )
        self.label.setFont(arctisSonarFonts.semiBold)
        self.hovered.connect(self.createHoverEffect)
        self.pressed.connect(self.onPressed)
        self.released.connect(self.onRelease)

        layout = QVBoxLayout()
        layout.addWidget(self.svgWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 4)
        effect.setColor(QColor(currentTheme.optionButtonBackground))
        effect.setBlurRadius(5)

        self.setGraphicsEffect(effect)
        self.setLayout(layout)

    def onPressed(self):
        self.currentBackgroundColor = self.onClickColor
        self.update()

    def onRelease(self):
        self.currentBackgroundColor = self.backgroundColor
        self.update()

    def enterEvent(self, event):
        self.hovered.emit(True)  # Emit the custom signal
        super().enterEvent(event)  # Call the base class method

        # Override the leaveEvent method to detect when the mouse leaves the button

    def leaveEvent(self, event):
        self.hovered.emit(False)  # Emit the custom signal
        super().leaveEvent(event)  # Call the base class method

    def createHoverEffect(self, hovered):
        if not self.isDown():
            if hovered:
                self.currentBorderWidth = self.borderWidth + 2
                self.currentBorderColor = self.hoverColor
            else:
                self.currentBorderWidth = self.borderWidth
                self.currentBorderColor = self.borderColor
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        background_color = QColor(returnColourCode(self.currentBackgroundColor))
        painter.setBrush(QBrush(background_color))

        # Set the border color and thickness
        border_color = QColor(returnColourCode(self.currentBorderColor))
        pen = QPen(border_color)
        pen.setWidth(self.currentBorderWidth)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw the button rectangle with background and border
        painter.drawRoundedRect(self.rect(), self.borderRadius, self.borderRadius)

    def sizeHint(self):
        return QSize(70, 70)  # Suggest a size for the button

    def setFixedSize(self, a0):
        svgSize = QSize(
            a0.width() - self.paddingSize,
            a0.height() - self.paddingSize
        )
        self.svgWidget.setFixedSize(svgSize)

        super().setFixedSize(a0)

    def changeSVGColor(self, color):
        self.svgWidget.updateColor(color)
        self.update()  # Refresh the button to repaint with the new widget

class CustomDialog(QDialog):
    def __init__(self, title, description, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle(title)

        title = QLabel(title)
        title.setFont(arctisSonarFonts.header3)

        description = QLabel(description)
        description.setWordWrap(True)
        description.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(description, stretch=1)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setFixedWidth(self.sizeHint().width())
        self.setFixedHeight(self.sizeHint().height())


class RoundedButton(QAbstractButton):
    """
    A custom button with rounded corners and a hover effect.
    """
    hovered = pyqtSignal(bool)

    def __init__(self,
                 label: str,
                 labelColor=currentTheme.primaryTextColour,
                 backgroundColor=currentTheme.primaryButtonColour,
                 borderColor="transparent",
                 borderRadius=3,
                 borderWidth=0,
                 onClickColor=currentTheme.activePrimaryButtonColour,
                 hoverColor=currentTheme.hoverColour,
                 *args, **kwargs):
        """
        Initialize the rounded button with the given parameters.
        :param label: The text label of the button.
        :param labelColor: The color of the label text.
        :param backgroundColor: The background color of the button.
        :param borderColor: The border color of the button.
        :param borderRadius: The radius of the button's rounded corners.
        :param borderWidth: The width of the button's border.
        :param onClickColor: The background color of the button when it is clicked.
        :param args: Additional arguments for the QAbstractButton constructor.
        :param kwargs: Additional keyword arguments for the QAbstractButton constructor.
        """

        super(RoundedButton, self).__init__(*args, **kwargs)

        self.label = label
        self.labelColor = labelColor
        self.labelFont = arctisSonarFonts.normal
        self.backgroundColor = backgroundColor
        self.onClickColor = onClickColor
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.borderRadius = borderRadius
        self.hoverColor = hoverColor

        self.originalBackgroundColor = backgroundColor
        self.originalHoverColor = self.hoverColor

        self.currentBackgroundColor = backgroundColor
        self.currentBorderWidth = self.borderWidth
        self.currentBorderColor = self.borderColor

        self.colorLabel = ColorLabel(
            text=self.label,
            textColor=self.labelColor,
            font=self.labelFont
        )

        self.hovered.connect(self.createHoverEffect)
        self.pressed.connect(self.onPressed)
        self.released.connect(self.onRelease)

        layout = QHBoxLayout()
        layout.addWidget(self.colorLabel, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
        self.setLayout(layout)

    def setEnabled(self, a0):
        if a0:
            self.currentBackgroundColor = self.originalBackgroundColor
            self.hoverColor = self.originalHoverColor
        else:
            self.currentBackgroundColor = currentTheme.disabledColour
            self.hoverColor = currentTheme.disabledColour
        super().setEnabled(a0)
        self.update()

    def onPressed(self):
        self.currentBackgroundColor = self.onClickColor
        self.update()

    def onRelease(self):
        self.currentBackgroundColor = self.backgroundColor
        self.update()

    def enterEvent(self, event):
        self.hovered.emit(True)  # Emit the custom signal
        super().enterEvent(event)  # Call the base class method

        # Override the leaveEvent method to detect when the mouse leaves the button

    def leaveEvent(self, event):
        self.hovered.emit(False)  # Emit the custom signal
        super().leaveEvent(event)  # Call the base class method

    def changeButtonLabel(self, text, color=None):
        if color != None:
            self.labelColor = color
        self.colorLabel.updateText(text, self.labelColor)

    def changeButtonColor(self, backgroundColor=None, hoverColor=None, onClickColor=None):
        if backgroundColor != None:
            self.originalBackgroundColor = backgroundColor
            self.currentBackgroundColor = backgroundColor
        if hoverColor != None:
            self.originalHoverColor = hoverColor
        if onClickColor != None:
            self.onClickColor = onClickColor
        self.update()

    def createHoverEffect(self, hovered):
        if not self.isDown():
            if hovered:
                self.currentBorderWidth = self.borderWidth + 2
                self.currentBorderColor = self.hoverColor
            else:
                self.currentBorderWidth = self.borderWidth
                self.currentBorderColor = self.borderColor
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        background_color = QColor(returnColourCode(self.currentBackgroundColor))
        painter.setBrush(QBrush(background_color))

        # Set the border color and thickness
        border_color = QColor(returnColourCode(self.currentBorderColor))
        pen = QPen(border_color)
        pen.setWidth(self.currentBorderWidth)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw the button rectangle with background and border
        painter.drawRoundedRect(self.rect(), self.borderRadius, self.borderRadius)

    def sizeHint(self):
        return QSize(111, 38)  # Suggest a size for the button

    def setFixedSize(self, a0):
        super().setFixedSize(a0)


class HeadphoneButton(QAbstractButton):
    hovered = pyqtSignal(bool)
    """
    An icon button with an SVG and a customizable background color.
    """

    def __init__(self,
                 device:ArctisDevice,
                 *args, **kwargs):

        """
        Initialize the button with the given SVG, color, background color, border color, border width, border radius, and hover color.
        :param svg: The SVG file to be displayed inside the button.
        :param svgColor: The color of the SVG.
        :param backgroundColor: The background color of the button.
        :param borderColor: The border color of the button.
        :param borderRadius: The radius of the button's border.
        :param borderWidth: The width of the button's border.
        :param onClickColor: The color to apply when the button is clicked.
        """
        super(HeadphoneButton, self).__init__(*args, **kwargs)


        self.device:ArctisDevice = device
        self.backgroundColor = currentTheme.hoverColour
        self.onClickColor = currentTheme.pressedPrimaryButtonColour
        self.borderRadius = 5
        self.hoverColor = "black"
        try:
            self.hoverColor = darken_color(self.onClickColor)
        except Exception as e:
            print(e)

        self.currentBackgroundColor = self.backgroundColor

        self.svgWidget = CustomSvgWidget(arctisSonarIcons.headphoneIcon, returnColourCode(currentTheme.activeColour) if device.isActive else returnColourCode(currentTheme.disabledColour) )
        self.svgWidget.setFixedSize(QSize(37,40))
        self.label = ColorLabel(
            text=device.name,
            textColor=currentTheme.primaryTextColour,
            font=arctisSonarFonts.semiBold
        )
        self.label.setFont(arctisSonarFonts.semiBold)
        self.hovered.connect(self.createHoverEffect)
        self.pressed.connect(self.onPressed)
        self.released.connect(self.onRelease)

        self.deviceIDVendorLabel = ColorLabel(
            text=hex(device.idVendor),
            textColor=currentTheme.disabledTextColour,
            font=arctisSonarFonts.normalSmallBold
        )
        self.deviceIDProductLabel = ColorLabel(
            text=hex(device.idProduct),
            textColor=currentTheme.disabledTextColour,
            font=arctisSonarFonts.normalSmallBold
        )

        deviceDetailsFormLayout = QFormLayout()
        deviceDetailsFormLayout.addRow(BoldLabel("Vendor ID:",font=arctisSonarFonts.normalSmallBold), self.deviceIDVendorLabel)
        deviceDetailsFormLayout.addRow(BoldLabel("Product ID:",font=arctisSonarFonts.normalSmallBold), self.deviceIDProductLabel)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignLeft)
        rightLayout.addLayout(deviceDetailsFormLayout, stretch = 1)

        rightWidget = QWidget()
        rightWidget.setLayout(rightLayout)

        layout = QHBoxLayout()
        layout.addWidget(self.svgWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rightWidget, stretch = 1)
        layout.setSpacing(25)

        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 4)
        effect.setBlurRadius(15)

        self.setGraphicsEffect(effect)

        self.setLayout(layout)

    def onPressed(self):
        self.currentBackgroundColor = self.onClickColor
        self.update()

    def onRelease(self):
        self.currentBackgroundColor = self.backgroundColor
        self.update()

    def enterEvent(self, event):
        self.hovered.emit(True)  # Emit the custom signal
        super().enterEvent(event)  # Call the base class method

        # Override the leaveEvent method to detect when the mouse leaves the button

    def leaveEvent(self, event):
        self.hovered.emit(False)  # Emit the custom signal
        super().leaveEvent(event)  # Call the base class method

    def createHoverEffect(self, hovered):
        if not self.isDown():
            self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        background_color = QColor(returnColourCode(self.currentBackgroundColor))
        painter.setBrush(QBrush(background_color))

        # Set the border color and thickness
        border_color = QColor("transparent")
        pen = QPen(border_color)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # Draw the button rectangle with background and border
        painter.drawRoundedRect(self.rect(), self.borderRadius, self.borderRadius)

    def changeSVGColor(self, color):
        self.svgWidget.updateColor(color)
        self.update()  # Refresh the button to repaint with the new widget

class VolumeLevelFrame(QWidget):
    def __init__(self, volumeLevel, *args, **kwargs):
        super(VolumeLevelFrame, self).__init__(*args, **kwargs)

        self.volumeLevelLabel = ColorLabel(
            text=f"{volumeLevel}%",
            font=arctisSonarFonts.semiBold,
            textColor=currentTheme.primaryTextColour
        )

        self.setFixedHeight(45)

        layout = QHBoxLayout()
        layout.addWidget(self.volumeLevelLabel, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)

        effect = QGraphicsDropShadowEffect()
        effect.setColor(QColor(currentTheme.disabledColour))
        effect.setOffset(0, 4)
        effect.setBlurRadius(15)

        self.setGraphicsEffect(effect)
        self.setLayout(layout)

    def setVolumeLevel(self, volumeLevel, colour):
        self.volumeLevelLabel.updateText(f"{volumeLevel}%", returnColourCode(colour))

    def paintEvent(self, e):
        painter = QPainter(self)
        background_color = QColor("#222931")
        painter.setBrush(QBrush(background_color))

        border_color = QColor("transparent")
        pen = QPen(border_color)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawRect(self.rect())

class AudioDeviceFrame(QWidget):
    def __init__(self, name, icon, colour, volumeRangeColours={0: "#08302B", 70: "#138F80", 100: "green"}, volumeLevel = 0, *args, **kwargs):
        super(AudioDeviceFrame, self).__init__(*args, **kwargs)
        self.name = name
        self.icon = icon
        self.colour = colour
        self.volumeRangeColours = volumeRangeColours
        self.volumeLevel = volumeLevel

        iconSVG = CustomSvgWidget(self.icon, returnColourCode(self.colour))
        iconSVG.setFixedSize(QSize(30,30))

        frameLabel = ColorLabel(
            text=f"{name}",
            font=arctisSonarFonts.normalBold,
            textColor=returnColourCode(self.colour)
        )

        self.volumeLevelFrame = VolumeLevelFrame(
            volumeLevel=self.volumeLevel,
        )

        self.volumeSlider = CustomProgressBar(colorRanges=volumeRangeColours)
        self.volumeSlider.setValue(self.volumeLevel)
        self.volumeSlider.setOrientation(Qt.Orientation.Vertical)
        self.volumeSlider.setEnabled(False)

        labelLayout = QHBoxLayout()
        labelLayout.addStretch()
        labelLayout.addWidget(iconSVG, alignment=Qt.AlignmentFlag.AlignVCenter)
        labelLayout.addWidget(frameLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        labelLayout.addStretch()
        labelLayout.setSpacing(10)

        layout = QVBoxLayout()
        layout.addLayout(labelLayout)
        layout.addWidget(self.volumeLevelFrame)
        layout.addWidget(self.volumeSlider, stretch=1, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setFixedWidth(282)
        self.setMaximumHeight(709)

        self.setLayout(layout)

    def setVolume(self, volumeLevel):
        color = "white"
        keyList = list(self.volumeRangeColours.keys())
        rangeCount = len(keyList)
        for i in range(0, rangeCount):
            minColorRange = keyList[i]
            maxColorRange = 100
            if i + 1 < rangeCount:
                maxColorRange = keyList[i + 1]
            if minColorRange <= volumeLevel and volumeLevel <= maxColorRange:
                color = self.volumeRangeColours[minColorRange]

        self.volumeLevelFrame.setVolumeLevel(volumeLevel, color)
        self.volumeSlider.setValue(volumeLevel)

    def paintEvent(self, e):
        painter = QPainter(self)
        background_color = QColor(currentTheme.audioDeviceFrameColour)
        painter.setBrush(QBrush(background_color))

        border_color = QColor("transparent")
        pen = QPen(border_color)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.drawRoundedRect(self.rect(), 10, 10)

class ChangeLogDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ChangeLogDialog,self).__init__(*args, **kwargs)
        self.setWindowTitle("SkyTestTool Update!")
        changeLogFilePath = f"{arctis_sonar_globals.arctisSonarGUI.returnApplicationPath()}/changeLog.md"
        if not os.path.isfile(changeLogFilePath):
            self.close()

        f = open(changeLogFilePath, 'r')
        self.markdownText = markdown.markdown(f.read())

        titleLabel = QLabel(f"ArctisSonarGUI v{arctis_sonar_globals.arctisSonarGUI.buildVersion}")
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLabel.setFont(arctisSonarFonts.header2)

        self.changeLogText = QLabel(self.markdownText)
        self.changeLogText.setContentsMargins(5,5,5,5)

        scrollArea = QScrollArea(self)
        scrollArea.setWidget(self.changeLogText)
        scrollArea.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(scrollArea, stretch=1)

        self.setLayout(layout)

def returnColourCode(color):
    """
    Returns a color code based on the given color string. If color code is not recognized, it returns the original color string.

    :param color: The color string.
    :return: The color code as a string.
    """
    color_dict = {
        "white": "#FFFFFF",
        "black": "#000000",
        "red": "#DA0000",
        "green": "#0C9700",
        "blue": "#0000FF",
        "yellow": "#FFFF00",
        "cyan": "#00FFFF",
        "magenta": "#FF00FF",
        "gray": "#808080",
        "silver": "#C0C0C0",
        "maroon": "#800000",
        "olive": "#808000",
        "purple": "#800080",
        "teal": "#008080",
        "navy": "#000080",
        "orange": "#FFA500",
        "pink": "#FFC0CB",
        "brown": "#A52A2A",
        "gold": "#FFD700",
        "amber": "#FFBF00"
    }
    return color_dict.get(color.lower(), color)

def darken_color(hex_color, factor=0.8):
    """
    Darkens a given hexadecimal color by a specified factor.

    :param hex_color: A string representing a hexadecimal color code, e.g., '#AABBCC'.
    :param factor: A float between 0 and 1 that determines how much to darken the color.
                   (0 = completely black, 1 = original color). Default is 0.8 (20% darker).
    :return: A new hexadecimal string of the darkened color.
    """
    if hex_color[0] != "#":
        hex_color = returnColourCode(hex_color)

    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')

    # Convert the hex color to RGB components
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Darken each component by multiplying it by the factor
    darkened_rgb = tuple(max(0, int(c * factor)) for c in rgb)

    # Convert the RGB components back to a hex string and return
    return '#{:02x}{:02x}{:02x}'.format(*darkened_rgb)