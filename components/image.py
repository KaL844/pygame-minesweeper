from typing import TypedDict
import pygame
from components.component import Component
from utils.enum_types import AlignType

from utils.logger import Logger
from utils.transform import TransformUtils

class ImageConf(TypedDict):
    src: str
    x: int
    y: int
    z: int
    width: int
    height: int
    anchor: AlignType
    isVisible: bool

class Image(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_SRC = None
    DEFAULT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True
    DEFAULT_WIDTH = -1
    DEFAULT_HEIGHT = -1

    logger = Logger(__name__).getInstance()

    def __init__(self, conf: ImageConf) -> None:
        super().__init__(conf['x'] if 'x' in conf else Image.DEFAULT_X, conf['y'] if 'y' in conf else Image.DEFAULT_Y, 
            conf['z'] if 'z' in conf else Image.DEFAULT_Z, conf['isVisible'] if 'isVisbile' in conf else Image.DEFAULT_VISIBLE)
        self.src = conf['src'] if 'src' in conf else Image.DEFAULT_SRC
        self.anchor = AlignType[conf['anchor']] if 'anchor' in conf else Image.DEFAULT_ANCHOR
        self.width = conf['width'] if 'width' in conf else Image.DEFAULT_WIDTH
        self.height = conf['height'] if 'height' in conf else Image.DEFAULT_HEIGHT
        
        self.image: pygame.surface.Surface = None

        self.loadImg()

    def draw(self, screen: pygame.surface.Surface) -> None:
        if self.image is None: return

        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.image.get_size()[0], self.image.get_size()[1])
        screen.blit(self.image, (posX, posY))

    def loadImg(self) -> None:
        if self.src is None:
            return
        self.image = pygame.image.load(self.src)
        width = self.image.get_size()[0] if self.width == Image.DEFAULT_WIDTH else self.width
        height = self.image.get_size()[1] if self.height == Image.DEFAULT_HEIGHT else self.height
        self.image = pygame.transform.scale(self.image, (width, height))

    def setSrc(self, src: str) -> None:
        self.src = src
        self.loadImg()
        