import pathlib
import configparser
from typing import Tuple, Union

import pygame

from tennessine.world import World
from tennessine.radarmap import RadarMap
from tennessine.sudoku import Sudoku
from tennessine.dialog import Dialog

root: pathlib.Path = pathlib.Path(__file__).parent.parent

config_parser: configparser.ConfigParser = configparser.ConfigParser()
config_parser.read(root / "config" / "config.ini")

RectValue = Tuple[
    Union[float, int], Union[float, int], Union[float, int], Union[float, int]
]


if __name__ == "__main__":
    pygame.init()
    clock: pygame.time.Clock = pygame.time.Clock()
    group: pygame.sprite.Group = pygame.sprite.Group()

    pygame.display.set_caption("Tennessine")
    screen: pygame.surface.Surface = pygame.display.set_mode(
        (
            config_parser.getint("window", "width"),
            config_parser.getint("window", "height"),
        )
    )

    world: World = World(
        (
            config_parser.getint("world", "width"),
            config_parser.getint("world", "height"),
        ),
        screen,
        str(root / "config" / "img" / config_parser.get("world", "background")),
    )

    radar_map: RadarMap = RadarMap(
        world,
        (
            config_parser.getint("radarmap", "width"),
            config_parser.getint("radarmap", "width")
            * world.image.get_height()
            / world.image.get_width(),
        ),
    )
    group.add(radar_map)

    dialog: Dialog = Dialog(
        (
            10,
            screen.get_height() - 310,
            screen.get_width() - 20,
            300,
        )
    )
    group.add(dialog)

    sudoku: Sudoku = Sudoku(
        (
            config_parser.getint("sudoku", "x", fallback=0),
            config_parser.getint("sudoku", "y", fallback=0),
            config_parser.getint("sudoku", "width"),
            config_parser.getint("sudoku", "height"),
        )
    )

    for cell in sudoku.board.board:
        group.add(cell)

    running: bool = True
    delay: float = 0

    fps: int = config_parser.getint("game", "fps")
    step: int = config_parser.getint("move", "step")
    x_offset: int = world.image.get_width() - screen.get_width()
    y_offset: int = world.image.get_height() - screen.get_height()

    mouse_position = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            world.visual_x -= step * delay
        if keys[pygame.K_RIGHT]:
            world.visual_x += step * delay
        if keys[pygame.K_UP]:
            world.visual_y -= step * delay
        if keys[pygame.K_DOWN]:
            world.visual_y += step * delay

        if world.visual_x > x_offset:
            world.visual_x = x_offset
        if world.visual_y > y_offset:
            world.visual_y = y_offset
        if world.visual_x < 0:
            world.visual_x = 0
        if world.visual_y < 0:
            world.visual_y = 0

        background: pygame.surface.Surface = world.image.subsurface(
            (world.visual_x, world.visual_y, screen.get_width(), screen.get_height())
        )
        screen.blit(background, (0, 0))

        group.update()
        group.draw(screen)
        pygame.display.flip()

        delay: float = clock.tick(fps) / 1000
    pygame.quit()
