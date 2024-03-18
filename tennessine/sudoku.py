import random
from typing import Iterable, Iterator, Tuple, List, Any

import pygame


class Cell(pygame.sprite.Sprite):
    number: int = 0

    def __init__(self, rect: Tuple[int, int, int, int], sudoku: "Sudoku") -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]
        self.font: pygame.font.Font = pygame.font.Font(
            pygame.font.get_default_font(), 70
        )
        self.draw()

    def draw(self) -> None:
        self.image.fill("#FFFFFF")
        pygame.draw.rect(self.image, "#000000", (0, 0, *self.rect[2:4]), 1)
        if self.number == 0:
            return
        text: pygame.surface.Surface = self.font.render(
            str(self.number), False, "#000000"
        )
        self.image.blit(text, (0, 0))

    def set(self, number: int) -> None:
        self.number = number
        self.draw()


class Board:
    def __init__(self, sudoku: "Sudoku") -> None:
        self.sudoku: "Sudoku" = sudoku
        self.board: List[Cell] = []
        for index in range(self.sudoku.line**2):
            y, x = divmod(index, self.sudoku.line)
            self.board.append(
                Cell(
                    (
                        int(
                            x * self.sudoku.cell_width
                            + x // self.sudoku.base * self.sudoku.line_width
                            + 5
                        ),
                        int(
                            y * self.sudoku.cell_height
                            + y // self.sudoku.base * self.sudoku.line_height
                            + 5
                        ),
                        int(self.sudoku.cell_width - 10),
                        int(self.sudoku.cell_height - 10),
                    ),
                    sudoku,
                )
            )

    def __iter__(self) -> Iterator:
        for value in self.board:
            yield value.number

    def __getitem__(self, key: int) -> int:
        return self.board[key].number

    def __setitem__(self, key: int, value: int) -> None:
        self.board[key].set(value)

    def __deltiem__(self, key: int) -> None:
        del self.board[key]

    def append(self, cell: Cell) -> None:
        self.board.append(cell)


class Sudoku(pygame.sprite.Sprite):
    base: int = 3
    line: int = base**2

    def __init__(self, rect: Tuple[int, int, int, int], seed: Any = None) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]

        self.line_width: float = 10
        self.cell_width: float = (
            rect[2] - (self.base - 1) * self.line_width
        ) / self.line
        self.line_height: float = 10
        self.cell_height: float = (
            rect[3] - (self.base - 1) * self.line_height
        ) / self.line
        self.board: Board = Board(self)

        if not seed:
            seed = random.random()
        self.random: random.Random = random.Random(seed)
        self.generate(0)

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
        candidate_values: List[int] = [i for i in range(1, self.line + 1)]
        for index, value in enumerate(self.board):
            j, i = divmod(index, 9)
            if (
                # same column
                x == i
                # same line
                or y == j
                # same chunk
                or x // self.base * self.base
                <= i
                < x // self.base * self.base + self.base
                and y // self.base * self.base
                <= j
                < y // self.base * self.base + self.base
            ) and value in candidate_values:
                candidate_values.remove(value)
        return candidate_values
