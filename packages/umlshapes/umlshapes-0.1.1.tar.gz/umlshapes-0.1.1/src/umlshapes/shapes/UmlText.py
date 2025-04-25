
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import ColourDatabase
from wx import FONTSTYLE_ITALIC
from wx import FONTWEIGHT_BOLD
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL

from wx import Colour
from wx import Font
from wx import MemoryDC
from wx import Menu

from wx.lib.ogl import Shape
from wx.lib.ogl import TextShape

from pyutmodelv2.PyutText import PyutText

from umlshapes.preferences.UmlPreferences import UmlPreferences

from umlshapes.shapes.ControlPointMixin import ControlPointMixin

from umlshapes.types.UmlColor import UmlColor
from umlshapes.types.UmlFontFamily import UmlFontFamily

from umlshapes.UmlUtils import UmlUtils

CONTROL_POINT_SIZE: int = 4         # Make this a preference


class UmlText(ControlPointMixin, TextShape):
    MARGIN: int = 5

    def __init__(self, pyutText: PyutText, width: int = 0, height: int = 0):    # TODO make default text size a preference):

        self.logger: Logger = getLogger(__name__)

        w: int = width
        h: int = height

        # Use preferences to get initial size if not specified
        preferences: UmlPreferences = UmlPreferences()

        if width == 0:
            w = preferences.textDimensions.width
        if height == 0:
            h = preferences.textDimensions.height

        self._pyutText: PyutText = pyutText

        super().__init__(shape=self)
        TextShape.__init__(self, width=w, height=h)

        self.shadowOffsetX = 0      #
        self.shadowOffsetY = 0      #

        self._textFontFamily: UmlFontFamily = preferences.textFontFamily
        self._textSize:       int  = preferences.textFontSize
        self._isBold:         bool = preferences.textBold
        self._isItalicized:   bool = preferences.textItalicize

        self._defaultFont: Font = UmlUtils.defaultFont()
        self._textFont:    Font = self._defaultFont.GetBaseFont()

        self._redColor:   Colour = ColourDatabase().Find('Red')
        self._blackColor: Colour = ColourDatabase().Find('Black')

        self.AddText(pyutText.content)

        self._initializeTextFont()
        self._menu: Menu = cast(Menu, None)

        umlBackgroundColor: UmlColor = preferences.textBackGroundColor
        backgroundColor:    Colour   = Colour(UmlColor.toWxColor(umlBackgroundColor))

        self._brush: Brush = Brush(backgroundColor)
        self.SetDraggable(drag=True)
        self.SetCentreResize(False)

    def OnDraw(self, dc: MemoryDC):

        dc.SetBrush(self._brush)

        if self.Selected() is True:
            UmlUtils.drawSelectedRectangle(dc=dc, shape=self)

    def OnDrawContents(self, dc):

        if self.Selected() is True:
            self.SetTextColour('Red')
        else:
            self.SetTextColour('Black')

        super().OnDrawContents(dc=dc)

    @property
    def shadowOffsetX(self):
        return self._shadowOffsetX

    @shadowOffsetX.setter
    def shadowOffsetX(self, value):
        self._shadowOffsetX = value

    @property
    def shadowOffsetY(self):
        return self._shadowOffsetY

    @shadowOffsetY.setter
    def shadowOffsetY(self, value):
        self._shadowOffsetY = value

    @property
    def moveColor(self) -> Colour:
        return self._redColor

    @property
    def pyutText(self):
        return self._pyutText

    @pyutText.setter
    def pyutText(self, pyutText: PyutText):
        self._pyutText = pyutText

    @property
    def textSize(self) -> int:
        return self._textSize

    @textSize.setter
    def textSize(self, newSize: int):
        self._textSize = newSize

    @property
    def isBold(self) -> bool:
        return self._isBold

    @isBold.setter
    def isBold(self, newValue: bool):
        self._isBold = newValue

    @property
    def isItalicized(self) -> bool:
        return self._isItalicized

    @isItalicized.setter
    def isItalicized(self, newValue: bool):
        self._isItalicized = newValue

    @property
    def textFontFamily(self) -> UmlFontFamily:
        return self._textFontFamily

    @textFontFamily.setter
    def textFontFamily(self, newValue: UmlFontFamily):
        self._textFontFamily = newValue

    @property
    def textFont(self) -> Font:
        return self._textFont

    @textFont.setter
    def textFont(self, newFont: Font):
        self._textFont = newFont

    def addChild(self, shape: Shape):
        """
        The event handler for UML Control Points wants to know who its` parent is
        Args:
            shape:
        """
        self._children.append(shape)

    def _initializeTextFont(self):
        """
        Use the model to get other text attributes; We'll
        get what was specified or defaults
        """

        self._textFont.SetPointSize(self.textSize)

        if self.isBold is True:
            self._textFont.SetWeight(FONTWEIGHT_BOLD)
        if self.isItalicized is True:
            self._textFont.SetWeight(FONTWEIGHT_NORMAL)

        if self.isItalicized is True:
            self._textFont.SetStyle(FONTSTYLE_ITALIC)
        else:
            self._textFont.SetStyle(FONTSTYLE_NORMAL)

        self._textFont.SetPointSize(self.textSize)
        self._textFont.SetFamily(UmlUtils.umlFontFamilyToWxFontFamily(self.textFontFamily))

        self.SetFont(self._textFont)

    def __str__(self) -> str:
        return f'UmlText - modelId: `{self._pyutText.id}`'

    def __repr__(self):

        strMe: str = f"[UmlText  modelId: '{self._pyutText.id}']"
        return strMe
