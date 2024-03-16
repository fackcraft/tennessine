from typing import Tuple, List, Iterator

import pygame


class Dialog(pygame.sprite.Sprite):
    def __init__(self, rect: Tuple[int, int, int, int]) -> None:
        super().__init__()

        self.image: pygame.surface.Surface = pygame.surface.Surface(rect[2:4])
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.x, self.rect.y = rect[0:2]
        self.font: pygame.font.Font = pygame.font.Font(
            pygame.font.get_default_font(), 30
        )
        self.text: str = self.wrap(
            "Tennessine is a synthetic chemical element. It has symbol Ts and atomic number 117. It has the second-highest atomic number and joint-highest atomic mass of all known elements, and is the penultimate element of the 7th period of the periodic table."
        )
        self.draw()

    def draw(self) -> None:
        self.image.fill("#FFFFFF")
        pygame.draw.rect(self.image, "#000000", self.rect)
        for index, text in enumerate(self.text):
            font: pygame.surface.Surface = self.font.render(text, False, "#000000")
            self.image.blit(font, (0, index * 30))

    @staticmethod
    def wrap(text: str) -> List[str]:
        text_lines: List[str] = []
        current_character: int = 0
        # while length of remaining characters is greater than 40
        while len(text) - current_character - 1 >= 75:
            for index in range(current_character + 75, current_character, -1):
                # find the latest space in remaining characters
                if not text[index].isspace():
                    continue
                text_lines.append(text[current_character:index])
                current_character = index
                break
        text_lines.append(text[current_character:len(text) - 1])
        return text_lines

    def set(self, text: str) -> None:
        self.text: str = text
        self.draw()
