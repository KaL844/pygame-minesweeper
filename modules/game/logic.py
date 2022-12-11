import random


class GameLogic:
    BOARD_ROWS = 10
    BOARD_COLS = 10

    NUM_BOMBS = 20

    BOMB_VALUE = -1

    def __init__(self) -> None:
        self.board = [[None for _ in range(GameLogic.BOARD_COLS)] for _ in range(GameLogic.BOARD_ROWS)]

        self.dugCells: set[tuple(int, int)] = set()

        self.plantBombs()
        self.initValues()

    def plantBombs(self) -> None:
        availableCells: list[tuple[int, int]] = []
        for i in range(GameLogic.BOARD_ROWS):
            for j in range(GameLogic.BOARD_COLS):
                availableCells.append((i, j))

        for _ in range(GameLogic.NUM_BOMBS):
            index = random.randint(0, len(availableCells) - 1)
            row, col = availableCells[index]
            del availableCells[index]
            self.board[row][col] = GameLogic.BOMB_VALUE

    def initValues(self) -> None:
        for i in range(GameLogic.BOARD_ROWS):
            for j in range(GameLogic.BOARD_COLS):
                if self.board[i][j] == GameLogic.BOMB_VALUE: continue
                self.board[i][j] = self.countBombsInNeighbor(i, j)

    def countBombsInNeighbor(self, row: int, col: int) -> int: 
        count = 0
        for i in range(max(0, row - 1), min(len(self.board), row + 2)):
            for j in range(max(0, col - 1), min(len(self.board[row]), col + 2)):
                if i == row and j == col: continue
                if self.board[i][j] == GameLogic.BOMB_VALUE: count += 1

        return count

    def getCell(self, row: int, col: int) -> int:
        return self.board[row][col]

    def dig(self, row: int, col: int, cells: list[tuple[int, int]]) -> bool:
        cells.append((row, col))
        self.dugCells.add((row, col))

        if self.board[row][col] == GameLogic.BOMB_VALUE: return False

        if self.board[row][col] != 0: return True
        for i in range(max(0, row - 1), min(len(self.board), row + 2)):
            for j in range(max(0, col - 1), min(len(self.board[row]), col + 2)):
                if (i, j) in self.dugCells or self.board[i][j] == GameLogic.BOMB_VALUE: continue
                self.dig(i, j, cells)

        return True

    def isEndGame(self) -> bool:
        for i in range(GameLogic.BOARD_ROWS):
            for j in range(GameLogic.BOARD_COLS):
                if self.board[i][j] != GameLogic.BOMB_VALUE and (i, j) not in self.dugCells: return False
        return True
                
                