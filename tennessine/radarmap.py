from typing import Tuple, Union

import pygame

from tennessine.world import World


class RadarMap(pygame.sprite.Sprite):
    def __init__(
        self, world: World, rect: Tuple[Union[float, int], Union[float, int]]
    ) -> None:
        super().__init__()
        self.world: World = world
        self.image: pygame.surface.Surface = pygame.transform.scale(world.image, rect)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        # northeast corner
        self.rect.x = world.screen.get_width() - self.image.get_width()

    def update(self) -> None:
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
