import pygame
import numpy
from algorithms.movement.bfs import a_star
from algorithms.movement.bfs import State
from interface.board import Board
from models.object import Object

original_image = pygame.image.load("resources/forklift.png")


class Forklift(Object):
    def __init__(self, board: Board):
        super().__init__(board)
        self.original_image = pygame.image.load("resources/forklift.png")
        self.image = pygame.transform.scale(
            self.original_image, (board.cell_size, board.cell_size)
        )
        self.direction = (-1, 0)
        self.rect = self.image.get_rect()
        self.rect.center = board.entity_map[board.width // 2][board.height // 2].center
        self.target_cell = None
        self.carried_objects: list = list()
        self.actions = []
        self.image_right = pygame.transform.flip(self.image, True, False)
        self.image_left = self.image
        self.image_up_left = pygame.transform.rotate(self.image, 90)
        self.image_up_right= pygame.transform.flip(self.image_up_left, True, False)
        self.image_down_left = pygame.transform.rotate(self.image, -90)
        self.image_down_right = pygame.transform.flip(self.image_down_left, True, False)

    def move_to_random_cell(self, board: Board):
        self.target_cell = board.get_random_location()

    def move_forward(self, board: Board, direction: tuple[int, int]):
        new_x = self.rect.x + direction[0] * board.cell_size
        new_y = self.rect.y + direction[1] * board.cell_size
        if 0 <= new_x < board.width * board.cell_size and 0 <= new_y < board.height * board.cell_size:
            self.rect.x = new_x
            self.rect.y = new_y

    def move_up(self, board: Board):
        self.move_forward(board, (0, 1))
        if self.direction == (1, 0):  # W prawo
            self.image = self.image_up_right
        elif self.direction == (-1, 0):  # W lewo
            self.image = self.image_up_left

    def move_down(self, board: Board):
        self.move_forward(board, (0, -1))
        if self.direction == (1, 0):  # W prawo
            self.image = self.image_down_right
        elif self.direction == (-1, 0):  # W lewo
            self.image = self.image_down_left

    def move_left(self, board: Board):
        self.move_forward(board, (-1, 0))
        self.image = self.image_left

    def move_right(self, board: Board):
        self.move_forward(board, (1, 0))
        self.image = self.image_right

    def rotate_right(self):
        self.image = pygame.transform.rotate(self.image, -90)
        if self.direction[1] == 0:
            if self.direction[0] == 1:
                self.direction = (0, -1)
            else:
                self.direction = (0, 1)
        else:
            self.direction = (numpy.sign(self.direction[0]), 0)

    def rotate_left(self):
        self.image = pygame.transform.rotate(self.image, 90)
        if self.direction[1] == 0:
            if self.direction[0] == 1:
                self.direction = (0, 1)
            else:
                self.direction = (0, -1)
        else:
            self.direction = (-numpy.sign(self.direction[0]), 0)
    
    def change_direction(self, current_direction: int):
        self.image = pygame.transform.flip(self.image, True, False)
        self.direction = (numpy.sign(current_direction), self.direction[1])


    def set_target(self, target_cell: tuple[int, int], board: Board):
        self.target_cell = target_cell
        start_state = State(self.rect.x // board.cell_size, self.rect.y // board.cell_size, self.direction)
        goal_state = State(target_cell[0] // board.cell_size, target_cell[1] // board.cell_size, self.direction)
        result_node = a_star(start_state, goal_state, board.entity_map)
        if result_node:
            actions = []
            while result_node.parent is not None:
                actions.append(result_node.action)
                result_node = result_node.parent
              
            self.actions = actions[::-1]
           

    def update(self, board: Board):
        if len(self.actions) > 0:
            action = self.actions.pop(0)
            if action == "left":
                self.move_left(board)
            elif action == "right":
                self.move_right(board)
            elif action == "up":
                self.move_up(board)
            elif action == "down":
                self.move_down(board)
        elif self.target_cell:
            self.target_cell = None