from typing import List, Optional
import heapq
from algorithms.movement.state import State
from algorithms.movement.node import Node

def heuristic(state: State, goal_state: State):
    cost = abs(state.x - goal_state.x) + abs(state.y - goal_state.y)
    shelf_positions = [(3, 0), (7, 0), (11, 0), (3, 9), (7, 9), (11, 9)]
    if (state.x, state.y) in shelf_positions:  
        cost += 100
    return cost


direction_map = {
    (1, 0): 'right',
    (-1, 0): 'left',
    (0, 1): 'up',
    (0, -1): 'down'
}

def get_action(dx, dy):
    return direction_map.get((dx, dy), 'unknown')

def find_neighbors(node: Node, search_grid: List[List[int]]) -> List[Node]:
    neighbors = []
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up
    for dx, dy in movements:
        new_x = node.state.x + dx
        new_y = node.state.y + dy
        new_direction = (dx, dy)
        if (
            0 <= new_x < len(search_grid)
            and 0 <= new_y < len(search_grid[0])
        ):
            new_state = State(new_x, new_y, new_direction)
            action = get_action(dx, dy)
            neighbors.append(Node(new_state, action))  

    return neighbors


def a_star(start_state: State, goal_state: State, search_grid: List[List[int]]) -> Optional[Node]:
    start_node = Node(start_state, cost=0, priority=heuristic(start_state, goal_state))
    fringe = []
    heapq.heappush(fringe, start_node)
    visited = set()
    visited.add(start_state)

    while fringe:
        current_node = heapq.heappop(fringe)
        if current_node.state == goal_state:
            return current_node

        neighbors = find_neighbors(current_node, search_grid)
        if neighbors ==[]:
            return False
        for neighbor in neighbors:
            if neighbor.state not in visited:
                neighbor.cost = current_node.cost + 1 
                neighbor.priority = neighbor.cost + heuristic(neighbor.state, goal_state)
                neighbor.parent = current_node
                heapq.heappush(fringe, neighbor)
                visited.add(neighbor.state)
        

    return None
