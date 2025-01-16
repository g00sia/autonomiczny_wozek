import os
import random
import pygame
from interface.board import Board


class Object(pygame.sprite.Sprite):
    def __init__(self, board: Board):
        super().__init__()
        self.image_path = self.load_random_image()
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (board.cell_size, board.cell_size)
        )
        self.rect = self.image.get_rect()
        self.rect.center = board.get_random_location()
        self.target_cell = None

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def load_random_image(self):
        resources_dir = "resources/items"
        image_files = os.listdir(resources_dir)
        random_image = random.choice(image_files)
        return os.path.join(resources_dir, random_image)
