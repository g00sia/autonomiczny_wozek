import pygame
import algorithms.decision_tree.decisionTree as decisionTree
import algorithms.neural_network.NeuralNetwork as neural_network
from algorithms import object_spawning
from interface.sidebar import SideBar
from interface.board import Board
from models.Forklift import Forklift
from models.Shelf import Shelf
from algorithms.genetic_algorithm import  genetic_a

BACKGROUND_COLOR = (255, 255, 255)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 10

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MONDRY_WOZEK")

    board = Board(board_height=10, board_width=15, screen=screen)
    side_bar = SideBar(screen, 0, "select_item")

    objects = pygame.sprite.Group()
    forklift = Forklift(board)
    shelves = Shelf.create_fixed_shelves(board)
    spawned_objects_with_positions = object_spawning.spawn_objects_with_positions(board, 10)
    for obj, pos in spawned_objects_with_positions:
        if obj.rect.collidelist([object.rect for object in objects]) == -1 and obj.rect.collidelist([shelf.rect for shelf in shelves])==-1:
            objects.add(obj)
            board.entity_map[pos[0]][pos[1]] = obj.rect
    shelves_positions = [(shelf.rect.x // board.cell_size, shelf.rect.y // board.cell_size) for shelf in shelves]
    packages_positions = [(obj.rect.x // board.cell_size, obj.rect.y // board.cell_size) for obj in objects]        
    best_route = genetic_a.genetic_algorithm(packages_positions, (forklift.rect.x // board.cell_size, forklift.rect.y // board.cell_size))
    best_objects_order = [list(objects)[index] for index in best_route]
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)
        side_bar.show_side_bar()
        side_bar.number_of_packages = len(forklift.carried_objects)
        if forklift.target_cell is None:
            side_bar.current_state_of_forklift = "select_item"
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (side_bar.x * 1.06 < mouse_pos[0] < side_bar.x * 1.06 + 150) and (
                    side_bar.y * 0.8 < mouse_pos[1] < side_bar.y * 0.8 + 50
                ):
                    running = False

        board.draw(screen)

        if len(objects)<=3:
            spawned_objects_with_positions = object_spawning.spawn_objects_with_positions(board, 10)
            for obj, pos in spawned_objects_with_positions:
                if obj.rect.collidelist([object.rect for object in objects]) == -1 and obj.rect.collidelist([shelf.rect for shelf in shelves])==-1:
                    objects.add(obj)
                    if obj:
                        board.entity_map[pos[0]][pos[1]] = obj.rect

            packages_positions = [(obj.rect.x // board.cell_size, obj.rect.y // board.cell_size) for obj in objects]        
            best_route = genetic_a.genetic_algorithm(packages_positions, (forklift.rect.x // board.cell_size, forklift.rect.y // board.cell_size))    
            best_objects_order = [list(objects)[index] for index in best_route]    

        for shelf in shelves:
            if forklift.rect.colliderect(shelf.rect):
                for product in forklift.carried_objects:
                    if shelf.add_product_to_shelf(product):
                        forklift.carried_objects.remove(product)
                forklift.carried_objects = []
                forklift.target_cell = None
                side_bar.current_state_of_forklift = "select_item"

        for obj in objects:
            if forklift.rect.colliderect(obj.rect):
                print(f"it's probably {neural_network.predict(obj.image_path)}")
                forklift.carried_objects.append(obj)
                side_bar.current_package = obj
                objects.remove(obj)
            obj.update(board)
            obj.draw(screen)

        if len(forklift.carried_objects) > 0:
            obj = forklift.carried_objects[0]
            parameters = (
                obj.days_in_store,
                obj.weight,
                obj.material,
                obj.height,
                obj.width,
                obj.depth,
                obj.priority,
                obj.fragile
            )
            if (decisionTree.make_decision([parameters]) == 1 or len(forklift.carried_objects) > 5) and forklift.target_cell is None:
                best_route_s = genetic_a.genetic_algorithm(shelves_positions, (forklift.rect.x // board.cell_size, forklift.rect.y // board.cell_size))
                best_objects_order_s = [list(shelves)[index] for index in best_route_s]
                next_shelf = best_objects_order_s.pop(0)
                print("Oh, it's time to load it to the shelf!")
                target_shelf = next_shelf.rect.center
                forklift.set_target(target_shelf, board)
                side_bar.current_state_of_forklift = "move_to_shelf"
                
        if len(best_objects_order) > 0 and forklift.target_cell is None:
            next_object = best_objects_order.pop(0)  
            target_object = next_object.rect.center
            side_bar.current_package = objects.sprites()[0]
            forklift.set_target(target_object, board)
            side_bar.current_state_of_forklift = "move_to_item"

        forklift.update(board)
        forklift.draw(screen)

        shelves.draw(screen)

        pygame.display.flip()
        clock.tick_busy_loop(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()

