import configparser
from typing import Tuple

import pygame


def draw(surface: pygame.surface.Surface, file_name: str = "transgender_pride_flag.ini"):
    cp: configparser.ConfigParser = configparser.ConfigParser()
    cp.read(file_name)

    rlist = cp["background"]["rects"]
    rlist = rlist.split(",")
    rlist = map(str.strip, rlist)
    world_width: int = cp.getint("background", "width")
    world_height: int = cp.getint("background", "height")
    for form in rlist:
        sectname = "rect_%s" % form
        color: str = cp.get(sectname, "color")
        x: int = cp.getint(sectname, "x", fallback=0)
        y: int = cp.getint(sectname, "y", fallback=0)
        width: int = cp.getint(sectname, "width")
        height: int = cp.getint(sectname, "height")
        pygame.draw.rect(
            surface,
            color,
            (
                x * surface.get_width() / world_width,
                y * surface.get_height() / world_height,
                width * surface.get_width() / world_width,
                height * surface.get_height() / world_height,
            ),
        )


class World(pygame.sprite.Sprite):
    visual_x: int = 0
    visual_y: int = 0

    def __init__(self, size: Tuple[int, int], screen: pygame.surface.Surface, file_name: str = "transgender_pride_flag.ini") -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.Surface(size)
        self.screen: pygame.surface.Surface = screen
        draw(self.image, file_name)
