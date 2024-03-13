import configparser
from typing import Tuple

import pygame


def draw(surface: pygame.surface.Surface):
    cp: configparser.ConfigParser = configparser.ConfigParser()
    cp.read("gay_pride_flag.ini")

    rlist = cp["background"]["rects"]
    rlist = rlist.split(",")
    rlist = map(str.strip, rlist)
    wwidth: int = cp.getint("background", "width")
    wheight: int = cp.getint("background", "height")
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
                x * surface.get_width() / wwidth,
                y * surface.get_height() / wheight,
                width * surface.get_width() / wwidth,
                height * surface.get_height() / wheight,
            ),
        )


class World(pygame.sprite.Sprite):
    visual_x: int = 0
    visual_y: int = 0

    def __init__(self, size: Tuple[int, int], screen: pygame.surface.Surface) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.Surface(size)
        self.screen: pygame.surface.Surface = screen
        draw(self.image)
