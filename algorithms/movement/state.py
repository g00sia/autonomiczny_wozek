class State:
    def __init__(self, x: int, y: int, dir: tuple[int, int]):
        self.x = x
        self.y = y
        self.direction = dir
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direction == other.direction

    def __hash__(self):
        return hash((self.x, self.y, self.direction))

    def __lt__(self, other):
        return (self.x, self.y, self.direction) < (other.x, other.y, other.direction)
