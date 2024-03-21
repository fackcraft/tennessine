from typing import List, Tuple

import pygame


class Image:
    def __init__(self, file_name: str) -> None:
        self._data: List[Tuple[str, int, int, int, int]] = []
        self._load_image(file_name)

    def _load_image(self, file_name: str) -> None:
        with open(file_name, "r") as file:
            while True:
                line = file.readline()
                if not line:
                    break
                args: List[str] = line.split(" ")
                if args[0] == "img":
                    self.width: int = int(args[1])
                    self.height: int = int(args[2])
                elif args[0] == "rect":
                    self._data.append(
                        (
                            args[1],
                            int(args[2]),
                            int(args[3]),
                            int(args[4]),
                            int(args[5]),
                        )
                    )

    def draw(self, surface: pygame.surface.Surface):
        for color, width, height, x, y in self._data:
            pygame.draw.rect(
                surface,
                color,
                (
                    x * surface.get_width() / self.width,
                    y * surface.get_height() / self.height,
                    width * surface.get_width() / self.width,
                    height * surface.get_height() / self.height,
                ),
            )
