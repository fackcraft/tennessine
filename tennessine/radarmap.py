from typing import Tuple
import pygame

from tennessine.world import World


class RadarMap(pygame.sprite.Sprite):
    def __init__(self, world: World, size: Tuple[float, float]) -> None:
        super().__init__()
        self.world: World = world
        self.image: pygame.surface.Surface = pygame.transform.scale(world.image, size)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x = world.screen.get_width() - self.image.get_width()

    def _draw(self) -> None:
        self.image: pygame.surface.Surface = pygame.transform.scale(
            self.world.image, self.rect[2:4]
        )
        pygame.draw.rect(self.image, "#000000", (0, 0, *self.rect[2:4]), 1)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)
        self._draw()
        pygame.draw.rect(
            self.image,
            "#000000",
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
