import configparser
import logging
import logging.config
# tuple annotation is available in Python 3.9
from typing import Optional, Tuple, Union

import pygame


logging.config.fileConfig("log.ini")
logger: logging.Logger = logging.getLogger()

config: configparser.ConfigParser = configparser.ConfigParser()
config.read("config.ini")

x: int = 0
y: int = 0

# typing.TypeAlias annotation is available in Python 3.10
RectValue = Tuple[
    Union[float, int], Union[float, int], Union[float, int], Union[float, int]
]


def draw_background(
    surface: pygame.surface.Surface,
    rect: Optional[RectValue] = None,
) -> None:
    # match case statement is available in Python 3.10
    background: str = config.get("world", "background")
    if background == "transgender_flag":
        # draw_transgender_flag(surface, rect)
        return
    if background == "rainbow_flag":
        # draw_rainbow_flag(surface, rect)
        return
    logger.warning("")


class RadarMap(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.Surface(
            (
                config.getint("radarmap", "width"),
                config.getint("radarmap", "width")
                * config.getint("world", "height")
                / config.getint("world", "width"),
            )
        )
        draw_background(self.image)

        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x = config.getint("window", "width") - config.getint(
            "radarmap", "width"
        )

    def update(self) -> None:
        draw_background(self.image)
        pygame.draw.rect(
            self.image,
            (255, 255, 255),
            (
                self.image.get_width() * x / config.getint("world", "width"),
                self.image.get_height() * y / config.getint("world", "height"),
                self.image.get_width()
                * config.getint("window", "width")
                / config.getint("world", "width"),
                self.image.get_height()
                * config.getint("window", "height")
                / config.getint("world", "height"),
            ),
            1,
        )


if __name__ == "__main__":
    pygame.init()
    screen: pygame.surface.Surface = pygame.display.set_mode(
        (config.getint("window", "width"), config.getint("window", "height"))
    )
    world: pygame.surface.Surface = pygame.Surface(
        (config.getint("world", "width"), config.getint("world", "height"))
    )
    clock: pygame.time.Clock = pygame.time.Clock()
    draw_background(
        world, (0, 0, config.getint("world", "width"), config.getint("world", "height"))
    )
    group: pygame.sprite.Group = pygame.sprite.Group()
    radar_map: RadarMap = RadarMap()
    group.add(radar_map)
    running: bool = True
    delay: float = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if y - config.getint("move", "step") < 0:
                y: int = 0
            else:
                y -= config.getint("move", "step")
        if keys[pygame.K_LEFT]:
            if x - config.getint("move", "step") < 0:
                x: int = 0
            else:
                x -= config.getint("move", "step")
        if keys[pygame.K_DOWN]:
            if y + config.getint("move", "step") + config.getint(
                "window", "height"
            ) > config.getint("world", "height"):
                y: int = config.getint("world", "height") - config.getint(
                    "window", "height"
                )
            else:
                y += config.getint("move", "step")
        if keys[pygame.K_RIGHT]:
            if x + config.getint("move", "step") + config.getint(
                "window", "width"
            ) > config.getint("world", "width"):
                x: int = config.getint("world", "width") - config.getint(
                    "window", "width"
                )
            else:
                x += config.getint("move", "step")

        background: pygame.surface.Surface = world.subsurface(
            (x, y, config.getint("window", "width"), config.getint("window", "height"))
        )
        screen.blit(background, (0, 0))

        group.update()
        group.draw(screen)
        pygame.display.flip()

        delay: float = clock.tick(60) / 1000
    pygame.quit()
