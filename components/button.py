import pygame
import typing
from components.component import Component

from utils.enum_types import AlignType, MouseEvent, MouseEventContext
from utils.logger import Logger
from utils.transform import TransformUtils

pygame.init()
FONT = pygame.font.Font(None, 30)

class ButtonConf(typing.TypedDict):
    x: int; y: int; z: int
    text: str
    color: tuple[int, int, int]; textColor: tuple[int, int, int]
    width: int; height: int
    isVisible: bool
    anchor: AlignType

class Button(Component):
    DEFAULT_COLOR = (255, 255, 255)
    DEFAULT_TEXT_COLOR = (0, 0, 0)
    DEFAULT_TEXT = ""
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_WIDTH = 180
    DEFAULT_HEIGHT = 40
    DEFAULT_VISIBLE = True
    DEFAULT_ANCHOR = AlignType.TOP_LEFT

    logger = Logger(__name__).getInstance()

    def __init__(self, conf: ButtonConf) -> None:
        self.isClicked: bool = False
        self.eventListeners: dict[MouseEvent, typing.Callable[[MouseEventContext], None]] = {}

        Button.logger.info("Button.__init__. conf={}".format(conf))

        super().__init__(conf["x"] if "x" in conf else Button.DEFAULT_X, conf["y"] if "y" in conf else Button.DEFAULT_Y,
            conf["z"] if "z" in conf else Button.DEFAULT_Z, conf["isVisible"] if "isVisible" in conf else Button.DEFAULT_VISIBLE)
        self.text = conf["text"] if "text" in conf else Button.DEFAULT_TEXT
        self.color = tuple(conf["color"]) if "color" in conf else Button.DEFAULT_COLOR
        self.textColor = conf["textColor"] if "textColor" in conf else Button.DEFAULT_TEXT_COLOR
        self.width = conf["width"] if "width" in conf else Button.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else Button.DEFAULT_HEIGHT
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Button.DEFAULT_ANCHOR

        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(posX, posY, self.width, self.height)

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return

        pos = pygame.mouse.get_pos()
    
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
                self.isClicked = True
            
            if pygame.mouse.get_pressed()[0] == 0 and self.isClicked:
                self.isClicked = False
                if MouseEvent.ON_TOUCH_END in self.eventListeners: 
                    touchEndHanler: typing.Callable[[MouseEventContext], None] = self.eventListeners[MouseEvent.ON_TOUCH_END]
                    touchEndHanler({'x': pos[0], 'y': pos[1]})

        pygame.draw.rect(screen, self.color, self.rect)

        posX, posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.width, self.height)
        textImg = FONT.render(self.text, True, self.textColor)
        screen.blit(textImg, (posX + self.width // 2 - textImg.get_size()[0] // 2, posY + self.height // 2 - textImg.get_size()[1] // 2))

    def addEventListener(self, event: MouseEvent, handler: typing.Callable[[MouseEventContext], None]) -> None:
        self.eventListeners[event] = handler

    def setPosition(self, x: int, y: int) -> None:
        posX, posY = TransformUtils.alignAnchor(self.anchor, x, y, self.width, self.height)
        self.rect = pygame.Rect(posX, posY, self.width, self.height)
        return super().setPosition(x, y)
