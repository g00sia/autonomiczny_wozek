import os
import random
import pygame
from models.Material import Material
from interface.board import Board
from models.object import Object


class Product(Object):
    def __init__(self, board: Board, name, weight, material: Material, id, pos: tuple[int, int], days_in_store: int, height: int, width: int,
                 depth: int, priority, fragile: int):
        super().__init__(board)
        self.image_path = f"resources/items/{name}.png"
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (board.cell_size, board.cell_size)
        )
        self.id = id
        self.name = name
        self.weight = weight
        self.material = material
        self.days_in_store = days_in_store
        self.height = height
        self.width = width
        self.depth = depth
        self.priority = priority
        self.fragile = fragile
    
    def __str__(self):
        return f"Product: {self.name}, {self.weight}, {self.material}"
    
    def get_random_photo(self):
        match self.material:
            case Material.glass:
                dir = os.listdir("data/test/glass/")
                return f"data/test/glass/{random.choice(dir)}"
            case Material.paper:
                dir = os.listdir("data/test/paper/")
                return f"data/test/paper/{random.choice(dir)}"
            case Material.plastic:
                dir = os.listdir("data/test/plastic/")
                return f"data/test/plastic/{random.choice(dir)}"
            case _ :
                dir = os.listdir("data/test/numbers")
                return f"data/test/numbers/{random.choice(dir)}"
    
    