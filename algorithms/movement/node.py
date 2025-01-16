from algorithms.movement.state import State

class Node:
    def __init__(self, state: State, action=None, parent=None, cost:int=0, priority:int=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost = cost
        self.priority = priority
    
    def __repr__(self):
        return f"Node(State({self.state.x}, {self.state.y}, {self.state.direction}), {self.action})"

    def __lt__(self, other):
        return self.priority < other.priority