from typing import TypedDict
import pygame
from components.component import Component

from components.label import Label

from utils.enum_types import AlignType
from utils.transform import TransformUtils

class InputTextBoxConf(TypedDict):
    x: int; y: int; z: int
    width: int; height: int
    color: tuple[int, int, int]; textColor: tuple[int, int, int]
    borderWidth: int
    padding: tuple[int, int]
    textAnchor: AlignType
    align: AlignType
    isVisible: bool

class InputTextBox(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 40
    DEFAULT_BORDER_WIDTH = 2
    DEFAULT_PADDING = (0, 0)          # Left, top
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_ALIGN = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True

    def __init__(self, conf: InputTextBoxConf) -> None:
        self.text = ""

        super().__init__(conf["x"] if "x" in conf else InputTextBox.DEFAULT_X, conf["y"] if "y" in conf else InputTextBox.DEFAULT_Y, 
            conf['z'] if 'z' in conf else InputTextBox.DEFAULT_Z, conf["isVisible"] if "isVisible" in conf else InputTextBox.DEFAULT_VISIBLE)
        self.width = conf["width"] if "width" in conf else InputTextBox.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else InputTextBox.DEFAULT_HEIGHT
        self.color = tuple(conf["color"]) if "color" in conf else InputTextBox.DEFAULT_COLOR
        self.borderWidth = conf["borderWidth"] if "borderWidth" in conf else InputTextBox.DEFAULT_BORDER_WIDTH
        self.textColor = tuple(conf["textColor"]) if "textColor" in conf else InputTextBox.DEFAULT_TEXT_COLOR
        self.padding = tuple(conf["padding"]) if "padding" in conf else InputTextBox.DEFAULT_PADDING
        self.textAnchor = AlignType[conf["textAnchor"]] if "textAnchor" in conf else InputTextBox.DEFAULT_TEXT_ANCHOR
        self.align = AlignType[conf["align"]] if "align" in conf else InputTextBox.DEFAULT_ALIGN

        self.isActive = False
        self.isClicked = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        textPosX, textPosY = TransformUtils.alignContent(self.align, self.x + self.padding[0], self.y + self.padding[1],
            self.width - self.padding[0] * 2, self.height - self.padding[1] * 2)
        self.textLabel: Label = Label(color=self.textColor, x=textPosX, y=textPosY, anchor=self.textAnchor)

    def draw(self, screen: pygame.surface.Surface) -> None:
        pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
            self.isClicked = True
            self.isActive = self.rect.collidepoint(pos)
        
        if pygame.mouse.get_pressed()[0] == 0 and self.isClicked:
            self.isClicked = False

        self.textLabel.setText(self.text)
        self.textLabel.draw(screen)
        pygame.draw.rect(screen, self.color, self.rect, self.borderWidth)

    def pushText(self, text: str):
        if not self.isActive: return

        self.text += text

    def popText(self):
        if not self.isActive: return

        self.text = self.text[0:-1]

    def clearText(self):
        self.text = ""

    def getText(self):
        return self.text