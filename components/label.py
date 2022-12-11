from typing import TypedDict
import pygame
from components.component import Component

from utils.enum_types import AlignType
from utils.transform import TransformUtils

pygame.init()

class LabelConf(TypedDict):
    x: int; y: int; z: int
    color: tuple[int, int, int]
    font: pygame.font.Font
    text: str
    isSmooth: bool
    anchor: AlignType
    isVisible: bool

class Label(Component):
    DEFAULT_TEXT = ""
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_FONT = pygame.font.Font(None, 20)
    DEFAULT_SMOOTH = True
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True

    def __init__(self, conf: LabelConf) -> None:
        super().__init__(conf["x"] if "x" in conf else Label.DEFAULT_X, conf["y"] if "y" in conf else Label.DEFAULT_Y, 
            conf['z'] if 'z' in conf else Label.DEFAULT_Z, conf["isVisible"] if "isVisible" in conf else Label.DEFAULT_VISIBLE)
        self.text = conf["text"] if "text" in conf else Label.DEFAULT_TEXT
        self.color = tuple(conf["color"]) if "color" in conf else Label.DEFAULT_COLOR
        self.isSmooth = conf["isSmooth"] if "isSmooth" in conf else Label.DEFAULT_SMOOTH
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Label.DEFAULT_ANCHOR
        self.font = Label.DEFAULT_FONT

        self.font = self.font

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return
        
        textImg = self.font.render(self.text, self.isSmooth, self.color)
        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, textImg.get_size()[0], textImg.get_size()[1])
        screen.blit(textImg, (posX, posY))

    def setText(self, text: str) -> None:
        self.text = text

    def clearText(self) -> None:
        self.text = ""

    def getText(self) -> str:
        return self.text