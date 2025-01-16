import random
from interface.board import Board
from models.Package import Package
from models.Shelf import Shelf
from models.Product import Product
from models.Material import Material
from models.Size import Size


def spawnRandomObject(board: Board, positions):
    spawnedObject = random.choice(["package", "product"])
    match spawnedObject:
        case "package":
            return _getRandomPackage(board, positions)
        case "product":
            return _getRandomProduct(board, positions)
        case _:
            return None
        

def spawn_objects_with_positions(board: Board, count: int):
    positions = generate_random_positions(board, count)
    objects_with_positions = []
    for pos in positions:
        spawned_object = random.choice(["package", "product"])
        if spawned_object == "package":
            obj = _getRandomPackage(board, pos)
        elif spawned_object == "product":
            obj = _getRandomProduct(board, pos)
        objects_with_positions.append((obj, pos))
    return objects_with_positions
  


def _getRandomPackage(board: Board, positions: tuple[int, int]):
    size = random.choice([Size.small, Size.medium, Size.big])
    weight = random.randint(10, 50)
    material = random.choice([Material.glass, Material.plastic, Material.paper])
    days_in_store = random.randint(1, 40)
    match size:
        case Size.small:
            height = random.randint(1, 35)
            width = random.randint(1, 35)
            depth = random.randint(1, 35)
        case Size.medium:
            height = random.randint(36, 70)
            width = random.randint(36, 70)
            depth = random.randint(36, 70)
        case Size.big:
            height = random.randint(71, 100)
            width = random.randint(71, 100)
            depth = random.randint(71, 100)

    match days_in_store:
        case 1, 10:
            priority = 1
        case 11, 20:
            priority = 2
        case _:
            priority = 3

    position = generate_random_positions(board, 1)
    fragile = 1 if material == Material.glass else 0
    return Package(board, size, weight, position, material, days_in_store, height, width, depth, priority, fragile)




def _getRandomProduct(board: Board, positions: tuple[int, int]):
    name = random.choice(["water", "milk", "paper"])
    weight = random.randint(10, 50)
    id = random.randint(1, 100)
    material = random.choice([Material.glass, Material.plastic, Material.paper])
    days_in_store = random.randint(1, 40)
    height = random.randint(1, 100)
    width = random.randint(1, 100)
    depth = random.randint(1, 100)

    match days_in_store:
        case 1, 10:
            priority = 1
        case 11, 20:
            priority = 2
        case _:
            priority = 3

    fragile = 1 if material == Material.glass else 0
    return Product(board, name, weight, material, id, positions, days_in_store, height, width, depth, priority, fragile)
  

def generate_random_positions(board: Board, count: int):
    positions = []
    # shelves =  [(3, 0), (7, 0), (11, 0), (3, 9), (7, 9), (11, 9)] 
    while len(positions) < count:
        x = random.randint(1,  board.width - 1)
        y = random.randint(1, 9)
        pos = (x, y)
        if pos not in positions: #and pos not in shelves  :
            positions.append(pos)          
    return positions