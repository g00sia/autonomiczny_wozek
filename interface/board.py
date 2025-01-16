import random
import pygame


class Board:
    def __init__(
        self, board_width: int, board_height: int, screen: pygame.Surface
    ) -> None:
        self.width = board_width
        self.height = board_height
        self.cell_size = min(
            screen.get_width() // board_width, screen.get_height() // board_height
        )
        self.entity_map: list[list[pygame.Rect]] = [
            [
                pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                for y in range(board_height)
            ]
            for x in range(board_width)
        ]

    def draw(self, screen: pygame.Surface) -> None:
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size),
                    1,
                )

    def get_random_location(self):
        return random.choice(random.choice(self.entity_map)).center
