import random
from typing import Tuple, List, Any

import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, rect: Tuple[float, float, float, float]) -> None:
        super().__init__()

        # init user interface
        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]

        font: pygame.font.Font = pygame.font.Font(pygame.font.get_default_font(), 16)
        pygame.draw.rect(self.image, "#FF0000", (0, 0) + rect[2:4])
        text: pygame.surface.Surface = font.render("0", True, "#FFFFFF")

        self.image.blit(text, (0, 0))


class Board:
    def __init__(self) -> None:
        self.board: List[Cell] = []

    def __getitem__(self, key: int) -> Cell:
        return self.board[key]

    def __setitem__(self, key: int, value: Cell) -> None:
        self.board[key] = value

    def __deltiem__(self, key: int) -> None:
        raise RuntimeError

    def append(self, cell: Cell) -> None:
        self.board.append(cell)


class Sudoku(pygame.sprite.Sprite):
    base: int = 3
    line: int = base**2

    def __init__(self, rect: Tuple[int, int, int, int], seed: Any = None) -> None:
        super().__init__()

        # init user interface
        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]

        # size
        self.line_width: float = rect[2] / 64
        self.cell_width: float = (
            rect[2] - (self.base - 1) * self.line_width
        ) / self.line
        self.line_height: float = rect[3] / 64
        self.cell_height: float = (
            rect[3] - (self.base - 3) * self.line_height
        ) / self.line

        self.board: Board = Board()
        for index in range(self.line**2):
            y, x = divmod(index, self.line)
            self.board.append(Cell(
                (
                    x * self.cell_width + x // self.base * self.line_width + 5,
                    y * self.cell_height + y // self.base * self.line_height + 5,
                    self.cell_width - 5,
                    self.cell_height - 5,
                ),
            ))

        # sudoku generate
        if not seed:
            seed = random.random()
        self.random: random.Random = random.Random(seed)
        # self.generate(0)

    def generate(self, index: int) -> bool:
        y, x = divmod(index, self.line)
        candidate_values: List[int] = self.get_candidate_values(x, y)
        random.shuffle(candidate_values, self.random.random)
        # success if reach the end of table
        if index == self.line**2:
            return True
        # try all candidate values, skip if no candidate values
        for candidate_value in candidate_values:
            self.board[index] = candidate_value
            # success if the next cell success
            if self.generate(index + 1):
                return True
        # traceback if no available values
        self.board[index] = 0
        return False

    def get_candidate_values(self, x: int, y: int) -> List[int]:
        candidate_values: List[int] = [i for i in range(1, 10)]
        for index, value in enumerate(self.board):
            j, i = divmod(index, 9)
            if (
                # same column
                x == i
                # same line
                or y == j
                # same chunk
                or x // 3 * 3 <= i < x // 3 * 3 + 3
                and y // 3 * 3 <= j < y // 3 * 3 + 3
            ) and value in candidate_values:
                candidate_values.remove(value)
        return candidate_values
