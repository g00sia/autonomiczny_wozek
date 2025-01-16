import pygame
from interface.board import Board
from models.Material import Material
from models.Size import Size
from models.object import Object


class Shelf(Object):
    def __init__(self, board: Board, x, y, image_path, capacity):
        super().__init__(board)
        self.image_path = image_path
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (board.cell_size, board.cell_size)
        )
        self.rect = self.image.get_rect(topleft=(x * board.cell_size, y * board.cell_size))
        self.board = board
        self.capacity = capacity
        self.products_on_shelf = []

    def add_product_to_shelf(self, product):
        if len(self.products_on_shelf) < self.capacity:
            self.products_on_shelf.append(product)
            if len(self.products_on_shelf) > 0:
                self.image_path = 'resources/shelves/shelf1.png'
                self.original_image = pygame.image.load(self.image_path)
                self.image = pygame.transform.scale(
                    self.original_image, (self.board.cell_size, self.board.cell_size)
                )
            if len(self.products_on_shelf) > 5:
                self.image_path = 'resources/shelves/shelf2.png'
                self.original_image = pygame.image.load(self.image_path)
                self.image = pygame.transform.scale(
                    self.original_image, (self.board.cell_size, self.board.cell_size)
                )
            if len(self.products_on_shelf) > 10:
                self.image_path = 'resources/shelves/shelf3.png'
                self.original_image = pygame.image.load(self.image_path)
                self.image = pygame.transform.scale(
                    self.original_image, (self.board.cell_size, self.board.cell_size)
                )
            return True
        return False

    def remove_product_from_shelf(self, id):
        for product in self.products_on_shelf:
            if product.id == id:
                self.products_on_shelf.remove(product)
                return True
        return False
    
    @classmethod
    def create_fixed_shelves(cls, board):
        shelf_positions = [(3, 0), (7, 0), (11, 0), (3, 9), (7, 9), (11, 9)]  
        shelf_types = [
            Size.small,  
            Size.medium,  
            Size.big,  
            Material.paper,  
            Material.glass,  
            Material.plastic  
        ]
        shelves = pygame.sprite.Group()

        for pos in shelf_positions:
            x, y = pos
            shelf = cls(board, x, y, 'resources/shelves/shelf.png', capacity=10)
            shelves.add(shelf)

        return shelves
