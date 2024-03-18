import pathlib
import configparser
from typing import Tuple

import pygame

root: pathlib.Path = pathlib.Path(__file__).parent.parent


def _draw(
    surface: pygame.surface.Surface, file_name: str = "transgender_pride_flag.ini"
):
    config_parser: configparser.ConfigParser = configparser.ConfigParser()
    config_parser.read(root / "config" / "theme" / file_name)
    world_width: int = config_parser.getint("background", "width")
    world_height: int = config_parser.getint("background", "height")
    for form in map(str.strip, config_parser["background"]["rects"].split(",")):
        sectname = f"rect_{form}"
        pygame.draw.rect(
            surface,
            config_parser.get(sectname, "color"),
            (
                config_parser.getint(sectname, "x", fallback=0)
                * surface.get_width()
                / world_width,
                config_parser.getint(sectname, "y", fallback=0)
                * surface.get_height()
                / world_height,
                config_parser.getint(sectname, "width")
                * surface.get_width()
                / world_width,
                config_parser.getint(sectname, "height")
                * surface.get_height()
                / world_height,
            ),
        )


class World(pygame.sprite.Sprite):
    visual_x: float = 0.0
    visual_y: float = 0.0

    def __init__(
        self,
        size: Tuple[int, int],
        screen: pygame.surface.Surface,
        file_name: str = "transgender_pride_flag.ini",
    ) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.Surface(size)
        self.screen: pygame.surface.Surface = screen
        _draw(self.image, file_name)
