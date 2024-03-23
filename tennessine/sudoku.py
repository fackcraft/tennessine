import random
from typing import Tuple, List, Any

import pygame


BASE: int = 3
LINE: int = BASE**2


class Sudoku(pygame.sprite.Sprite):
    def __init__(self, rect: Tuple[int, int, int, int], seed: Any = None) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.image.fill("#FFAACC")
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]
        self._font: pygame.font.Font = pygame.font.Font(
            "/usr/share/fonts/TTF/FiraCodeNerdFontMono-Regular.ttf",
            70,
        )

        self._line_width: int = 10
        self._cell_width: int = (rect[2] - (BASE - 1) * self._line_width) // LINE
        self._line_height: int = 10
        self._cell_height: int = (rect[3] - (BASE - 1) * self._line_height) // LINE

        self._board: List[int] = [0] * LINE**2
        self._draw_all()

        if not seed:
            seed = random.random()
        self._random: random.Random = random.Random(seed)
        self._generate(0)

    def _draw_all(self) -> None:
        for index in range(LINE**2):
            self._board.append(0)
            self._draw(index)

    def _draw(self, index) -> None:
        y, x = divmod(index, LINE)
        rect: Tuple[int, int, int, int] = (
            x * self._cell_width + x // BASE * self._line_width + 5,
            y * self._cell_height + y // BASE * self._line_height + 5,
            self._cell_width - 10,
            self._cell_height - 10,
        )
        pygame.draw.rect(self.image, "#FFFFFF", rect)
        pygame.draw.rect(self.image, "#000000", rect, 1)
        if self._board[index] == 0:
            return
        text: pygame.surface.Surface = self._font.render(
            str(self._board[index]), False, "#000000"
        )
        self.image.blit(text, rect[:2])

    def _generate(self, index: int) -> bool:
        y, x = divmod(index, LINE)
        candidate_values: List[int] = self.get_candidate_values(x, y)
        random.shuffle(candidate_values, self._random.random)
        if index == LINE**2:
            return True
        for candidate_value in candidate_values:
            self._board[index] = candidate_value
            self._draw(index)
            if self._generate(index + 1):
                return True
        self._board[index] = 0
        self._draw(index)
        return False

    def get_candidate_values(self, x: int, y: int) -> List[int]:
        candidate_values: List[int] = [i for i in range(1, LINE + 1)]
        for index, value in enumerate(self._board):
            j, i = divmod(index, 9)
            if (
                x == i
                or y == j
                or x // BASE * BASE <= i < x // BASE * BASE + BASE
                and y // BASE * BASE <= j < y // BASE * BASE + BASE
            ) and value in candidate_values:
                candidate_values.remove(value)
        return candidate_values
