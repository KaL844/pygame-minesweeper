from typing import TypedDict
import typing
import pygame
from components.component import Component, ComponentType
from utils.enum_types import AlignType, MouseEvent, MouseEventContext
from utils.transform import TransformUtils

class PanelConf(TypedDict):
    x: int; y: int; z: int
    width: int; height: int
    backgroundColor: tuple[int, int, int, int]
    anchor: AlignType
    isVisible: bool
    children: dict

class Panel(Component):
    DEFAULT_X = 0
    DEFAULT_Y = 0
    DEFAULT_Z = 0
    DEFAULT_WIDTH = 0
    DEFAULT_HEIGHT = 0
    DEFAULT_BACKGROUND_COLOR = (0, 0, 0, 0)
    DEFAULT_ANCHOR = AlignType.TOP_LEFT
    DEFAULT_VISIBLE = True

    def __init__(self, conf: PanelConf) -> None:
        self.isClicked = False
        self.children: dict[str, Component] = {}
        self.eventListeners: dict[MouseEvent, typing.Callable[[MouseEventContext], None]] = {}

        super().__init__(conf["x"] if "x" in conf else Panel.DEFAULT_X, conf["y"] if "y" in conf else Panel.DEFAULT_Y, 
            conf['z'] if 'z' in conf else Panel.DEFAULT_Z, conf["isVisible"] if "isVisible" in conf else Panel.DEFAULT_VISIBLE)
        if "children" in conf:
            children: dict = conf["children"]
            for childName, child in children.items():
                self.addChild(childName, Component.getComponent(ComponentType[child["component"]], child))
        self.width = conf["width"] if "width" in conf else Panel.DEFAULT_WIDTH
        self.height = conf["height"] if "height" in conf else Panel.DEFAULT_HEIGHT
        self.backgroundColor = conf["backgroundColor"] if "backgroundColor" in conf else Panel.DEFAULT_BACKGROUND_COLOR
        self.anchor = AlignType[conf["anchor"]] if "anchor" in conf else Panel.DEFAULT_ANCHOR

        self.posX, self.posY = TransformUtils.alignAnchor(self.anchor, self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.rect.Rect(self.posX, self.posY, self.width, self.height)

    def draw(self, screen: pygame.surface.Surface) -> None:
        if not self.isVisible: return 

        self.surface.fill(self.backgroundColor)

        for child in sorted(self.children.values(), key=lambda child: child.getZ()):
            child.draw(self.surface)
        
        pos = pygame.mouse.get_pos()
    
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.isClicked:
                self.isClicked = True
            
            if pygame.mouse.get_pressed()[0] == 0 and self.isClicked:
                self.isClicked = False
                if MouseEvent.ON_TOUCH_END in self.eventListeners: 
                    touchEndHanler: typing.Callable[[MouseEventContext], None] = self.eventListeners[MouseEvent.ON_TOUCH_END]
                    touchEndHanler({'x': pos[0], 'y': pos[1]})

        screen.blit(self.surface, (self.posX, self.posY))

    def addChild(self, name: str, child: Component) -> None:
        self.children[name] = child

    def getChild(self, name: str) -> Component:
        if name in self.children: return self.children[name]

    def addEventListener(self, event: MouseEvent, handler: typing.Callable[[MouseEventContext], None]) -> None:
        self.eventListeners[event] = handler

    def getLocalPosition(self, x: int, y: int) -> tuple[int, int]:
        if x < self.posX or x > self.posX + self.width or y < self.posY or y > self.posY + self.height:
            return (-1, -1)
        return (x - self.posX, y - self.posY)

    def getSize(self) -> tuple[int, int]: 
        return (self.width, self.height)

    def clear(self) -> None:
        self.children = {}