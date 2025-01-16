import pygame

from models import Material
from models.object import Object
from interface.board import Board
from models.Product import Product
from models.Size import Size

class Package(Object):
    def __init__(self, board: Board, size: Size, weight: int, pos: tuple[int, int], material: Material, days_in_store: int, height: int,
                 width: int, depth: int, priority: int, fragile: int):
        super().__init__(board)
        self.image_path = self._choose_image(size)
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (board.cell_size, board.cell_size)
        )
        
        self.size = size
        self.weight = weight
        self.material = material
        self.days_in_store = days_in_store
        self.products = []
        self.height = height
        self.width = width
        self.depth = depth
        self.priority = priority
        self.fragile = fragile
        self.name = "paczka"
        
    def add_product(self, name, weight):
        product = Product(name, weight)
        self.products.append(product)

    def remove_product(self, name):
        for product in self.products:
            if product.name == name:
                self.products.remove(product)
                return True
        return False

    def total_weight(self):
        total = self.weight
        for product in self.products:
            total += product.weight
        return total

    def _choose_image(self, size: Size):
        if size == Size.small:
            return "resources/items/package.png"
        if size == Size.medium:
            return "resources/items/package2.png"
        if size == Size.big:
            return "resources/items/package3.png"
        
    def __str__(self):
        return f"Package: {self.size}, {self.weight}, {self.products}"
