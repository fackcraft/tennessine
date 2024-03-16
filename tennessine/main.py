import configparser
from typing import Tuple, Union

import pygame

from tennessine.world import World
from tennessine.radarmap import RadarMap
from tennessine.sudoku import Sudoku
from tennessine.dialog import Dialog

cp: configparser.ConfigParser = configparser.ConfigParser()
cp.read("config.ini")

RectValue = Tuple[
    Union[float, int], Union[float, int], Union[float, int], Union[float, int]
]

if __name__ == "__main__":
    pygame.init()
    clock: pygame.time.Clock = pygame.time.Clock()
    group: pygame.sprite.Group = pygame.sprite.Group()

    pygame.display.set_caption("Tennessine")
    screen: pygame.surface.Surface = pygame.display.set_mode(
        (cp.getint("window", "width"), cp.getint("window", "height"))
    )

    world: World = World(
        (cp.getint("world", "width"), cp.getint("world", "height")),
        screen,
        cp.get("world", "background", fallback="transgender_pride_flag.ini"),
    )

    radar_map: RadarMap = RadarMap(
        world,
        (
            cp.getint("radarmap", "width"),
            cp.getint("radarmap", "width")
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
            cp.getint("sudoku", "x", fallback=0),
            cp.getint("sudoku", "y", fallback=0),
            cp.getint("sudoku", "width"),
            cp.getint("sudoku", "height"),
        )
    )

    # for cell in sudoku.board.board:
    #     group.add(cell)

    running: bool = True
    delay: float = 0

    tps: int = cp.getint("game", "tps")
    step: int = cp.getint("move", "step")
    y_offset: int = world.image.get_height() - screen.get_height()
    x_offset: int = world.image.get_width() - screen.get_width()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            world.visual_x += step * delay
        if keys[pygame.K_DOWN]:
            world.visual_y += step * delay
        if keys[pygame.K_LEFT]:
            world.visual_x -= step * delay
        if keys[pygame.K_UP]:
            world.visual_y -= step * delay

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

        delay: float = clock.tick(tps) / 1000
    pygame.quit()
