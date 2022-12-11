import pygame
from components.scene import Scene, SceneManager
from components.button import Button
from modules.game.scenes import GameScene
from utils.enum_types import MouseEvent, MouseEventContext
from utils.json_reader import JsonReader
import utils.constants as constants


class StartScene(Scene):
    CONFIG_FILE = "conf/lobby/StartScene.json"

    def __init__(self) -> None:
        self.sceneMgr = None

        self.conf = JsonReader.load(StartScene.CONFIG_FILE)

        self.startBtn: Button = Button(conf=self.conf["startBtn"])

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()

        self.startBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onStartClick)

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)
        self.startBtn.draw(screen)

    def onStartClick(self, _: MouseEventContext) -> None:
        self.sceneMgr.push(GameScene())