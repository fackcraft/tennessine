import configparser
from typing import Tuple, Union

import pygame

from tennessine.world import World
from tennessine.radarmap import RadarMap

config: configparser.ConfigParser = configparser.ConfigParser()
config.read("config.ini")

RectValue = Tuple[
    Union[float, int], Union[float, int], Union[float, int], Union[float, int]
]

if __name__ == "__main__":
    pygame.init()
    screen: pygame.surface.Surface = pygame.display.set_mode(
        (config.getint("window", "width"), config.getint("window", "height"))
    )
    world: World = World(
        (config.getint("world", "width"), config.getint("world", "height")), screen
    )
    clock: pygame.time.Clock = pygame.time.Clock()
    group: pygame.sprite.Group = pygame.sprite.Group()
    radar_map: RadarMap = RadarMap(
        world,
        (
            config.getint("radarmap", "width"),
            config.getint("radarmap", "width")
            * world.image.get_height()
            / world.image.get_width(),
        ),
    )

    group.add(radar_map)
    running: bool = True
    delay: float = 0
    step: int = config.getint("move", "step")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if world.visual_y - step < 0:
                world.visual_y = 0
            else:
                world.visual_y -= step
        if keys[pygame.K_LEFT]:
            if world.visual_x - step < 0:
                world.visual_x = 0
            else:
                world.visual_x -= step
        if keys[pygame.K_DOWN]:
            if world.visual_y + step + screen.get_height() > world.image.get_height():
                world.visual_y = world.image.get_height() - screen.get_height()
            else:
                world.visual_y += step
        if keys[pygame.K_RIGHT]:
            if world.visual_x + step + screen.get_width() > world.image.get_width():
                world.visual_x = world.image.get_width() - screen.get_width()
            else:
                world.visual_x += step

        background: pygame.surface.Surface = world.image.subsurface(
            (world.visual_x, world.visual_y, screen.get_width(), screen.get_height())
        )
        screen.blit(background, (0, 0))

        group.update()
        group.draw(screen)
        pygame.display.flip()

        delay: float = clock.tick(60) / 1000
    pygame.quit()
