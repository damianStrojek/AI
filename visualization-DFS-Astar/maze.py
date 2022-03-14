import sys
from enum import Enum


class NodeType(Enum):
    NORMAL = ' ';
    NORMAL_VISITED = '.'
    SWAMP = '!';
    SWAMP_VISITED = '-'
    WALL = '#'
    START = 'S'
    GOAL = 'E'


class Node:
    def __init__(self, x, y, type_str=' '):
        self.x = x
        self.y = y
        self.type = NodeType(type_str)
        self.visited = False
        self.parent = None
        self.cost = sys.maxsize  # Inf

    def __str__(self):
        if self.type == NodeType.NORMAL and self.visited:
            return NodeType.NORMAL_VISITED.value
        elif self.type == NodeType.SWAMP and self.visited:
            return NodeType.SWAMP_VISITED.value
        else:
            return self.type.value

    def reset(self):
        self.visited = False
        self.parent = None
        self.cost = sys.maxsize


class Maze:
    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            maze = [[Node(x, y, char) for x, char in enumerate(line.strip())] for y, line in enumerate(f)]
        return cls(maze)

    def __init__(self, maze):
        self.maze = maze
        self.path = []

    def draw(self):
        for x_nodes in self.maze:
            for node in x_nodes:
                if node in self.path and node.type != NodeType.START and node.type != NodeType.GOAL:
                    print('*', end='')
                else:
                    print(node, end='')
            print()

    def find_node(self, type):
        for x_nodes in self.maze:
            for node in x_nodes:
                if node.type == type:
                    return node

    def get_possible_movements(self, node):
        possible_movements = []
        if node.y - 1 >= 0 and self.maze[node.y - 1][node.x].type != NodeType.WALL:  # north
            possible_movements.append(self.maze[node.y - 1][node.x])
        if node.x + 1 < len(self.maze[node.y]) and self.maze[node.y][node.x + 1].type != NodeType.WALL:  # east
            possible_movements.append(self.maze[node.y][node.x + 1])
        if node.y + 1 < len(self.maze) and self.maze[node.y + 1][node.x].type != NodeType.WALL:  # south
            possible_movements.append(self.maze[node.y + 1][node.x])
        if node.x - 1 >= 0 and self.maze[node.y][node.x - 1].type != NodeType.WALL:  # west
            possible_movements.append(self.maze[node.y][node.x - 1])

        return possible_movements

    @staticmethod
    def move_cost(n1):
        if n1.type == NodeType.SWAMP:
            return 5
        else:
            return 1

    @staticmethod
    def path_from(node):
        path = [node]
        while node.parent is not None:
            node = node.parent
            path.append(node)
        return path
