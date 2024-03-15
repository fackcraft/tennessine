from typing import Tuple, Union

import pygame

from tennessine.world import World


class RadarMap(pygame.sprite.Sprite):
    def __init__(
        self, world: World, size: Tuple[float, float]
    ) -> None:
        super().__init__()
        self.world: World = world
        self.image: pygame.surface.Surface = pygame.transform.scale(world.image, size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x = world.screen.get_width() - self.image.get_width()

    def update(self) -> None:
        self.image: pygame.surface.Surface = pygame.transform.scale(self.world.image, self.rect[2:4]
)
        pygame.draw.rect(
            self.image,
            (255, 255, 255),
            (
                self.image.get_width()
                * self.world.visual_x
                / self.world.image.get_width(),
                self.image.get_height()
                * self.world.visual_y
                / self.world.image.get_height(),
                self.image.get_width()
                * self.world.screen.get_width()
                / self.world.image.get_width(),
                self.image.get_height()
                * self.world.screen.get_height()
                / self.world.image.get_height(),
            ),
            1,
        )
