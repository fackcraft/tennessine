import pathlib
from typing import Tuple

import pygame

from tennessine.image import Image

root: pathlib.Path = pathlib.Path(__file__).parent.parent


class World(pygame.sprite.Sprite):
    visual_x: float = 0.0
    visual_y: float = 0.0

    def __init__(
        self,
        size: Tuple[int, int],
        screen: pygame.surface.Surface,
        file_name: str,
    ) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.Surface(size)
        self.screen: pygame.surface.Surface = screen
        image: Image = Image(file_name)
        image.draw(self.image)
