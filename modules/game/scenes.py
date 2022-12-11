import pygame
from components.button import Button
from components.label import Label
from components.scene import Scene, SceneManager
from components.panel import Panel
from components.shape import Line
from modules.game.logic import GameLogic
from utils.enum_types import MouseEvent, MouseEventContext
from utils.json_reader import JsonReader
import utils.constants as constants


class GameScene(Scene):
    CONFIG_FILE = "conf/game/GameScene.json"

    FLAG = '#'

    def __init__(self) -> None:
        self.conf = JsonReader.load(GameScene.CONFIG_FILE)

        self.logic = GameLogic()
        self.isDigging = True
        self.isRunning = True
        self.switchBtn = Button(conf=self.conf["switchBtn"])
        self.boardPanel = Panel(conf=self.conf["boardPanel"])
        self.modeLabel = Label(conf=self.conf["modeLabel"])
        self.endGamePanel: Panel = Panel(conf=self.conf["endGamePanel"])
        self.returnBtn: Button = self.endGamePanel.getChild("returnBtn")

        self.init()

    def init(self) -> None:
        self.sceneMgr = SceneManager.getInstance()
        self.modeLabel.setText("Dig" if self.isDigging else "Flag")
        self.returnBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onReturnClick)
        self.boardPanel.addEventListener(MouseEvent.ON_TOUCH_END, self.onBoardClick)
        self.switchBtn.addEventListener(MouseEvent.ON_TOUCH_END, self.onSwitchClick)
        self.width, self.height = self.boardPanel.getSize()
        self.cellWidth, self.cellHeight = self.width // GameLogic.BOARD_COLS, self.height // GameLogic.BOARD_ROWS
        self.addLines()
        self.addValues()

    def addLines(self) -> None:
        for i in range(GameLogic.BOARD_COLS + 1):
            offset = 0 if i == 0 else -2
            self.boardPanel.addChild(f"verticalLine{i}", Line({'startX': i * self.cellWidth + offset, 'endX': i * self.cellWidth + offset, 
                'startY': 0, 'endY': self.height, "width": 2}))
        for i in range(GameLogic.BOARD_ROWS + 1):
            offset = 0 if i == 0 else -2
            self.boardPanel.addChild(f"horizontalLine{i}", Line({'startX': 0, 'endX': self.width, 'startY': i * self.cellHeight + offset, 
                'endY': i * self.cellHeight + offset, "width": 2}))
    
    def addValues(self) -> None:
        for i in range(GameLogic.BOARD_ROWS):
            for j in range(GameLogic.BOARD_COLS):
                self.boardPanel.addChild(f"label_{i}_{j}", Label({'x': (j + 0.5) * self.cellWidth, 'y': (i + 0.5) * self.cellHeight, 
                    'text': str(self.logic.getCell(i, j)), 'anchor': 'MID_CENTER', 'isVisible': False}))

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(constants.BACKGROUND_COLOR)

        self.boardPanel.draw(screen)
        self.switchBtn.draw(screen)
        self.modeLabel.draw(screen)
        self.endGamePanel.draw(screen)

    def onBoardClick(self, context: MouseEventContext) -> None:
        if not self.isRunning: return

        x, y = context['x'], context['y']
        localX, localY = self.boardPanel.getLocalPosition(x, y)
        row, col = localY // self.cellHeight, localX // self.cellWidth

        if not self.isDigging:
            cell: Label = self.boardPanel.getChild(f"label_{row}_{col}")
            if cell.getText() == GameScene.FLAG:
                cell.setText(str(self.logic.getCell(row, col)))
                cell.setVisible(False)
                return
            cell.setText(GameScene.FLAG)
            cell.setVisible(True)
            return

        cells: list[tuple[int, int]] = []
        isSuccess = self.logic.dig(row, col, cells)
        for row, col in cells:
            self.boardPanel.getChild(f"label_{row}_{col}").setVisible(True)
        if not isSuccess or self.logic.isEndGame():
            self.endGame()
            return

    def onSwitchClick(self, _: MouseEventContext) -> None:
        if not self.isRunning: return
        self.isDigging = not self.isDigging
        self.modeLabel.setText("Dig" if self.isDigging else "Flag")

    def onReturnClick(self, _: MouseEventContext) -> None:
        self.sceneMgr.clear()
        from modules.lobby.scenes import StartScene
        self.sceneMgr.push(StartScene())

    def endGame(self) -> None:
        self.isRunning = False
        self.endGamePanel.setVisible(True)
