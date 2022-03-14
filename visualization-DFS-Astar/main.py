import argparse
from maze import Maze
from search_algos import algos_mapping


def print_result_info(maze, steps_required):
    print("Path:", end=" ")
    for node in maze.path:
        print(f'({node.x}, {node.y})', end=' ')
    print()
    print(f"Path found in: {steps_required} steps.")
    print(f"Path length: {len(maze.path)}")


def main_cli(algo, mazefile):
    maze = Maze.from_file(mazefile)
    maze.draw()
    maze.path, n_steps = algo(maze)
    print()
    maze.draw()
    print_result_info(maze, n_steps)


def main_gui(algo, mazefile):
    from gui import PyGameMaze, wait_for_quit
    maze = PyGameMaze.from_file(mazefile)
    maze.draw()
    maze.path, n_steps = algo(maze)
    maze.draw()
    print_result_info(maze, n_steps)
    wait_for_quit()


if __name__ == '__main__':
    main_gui(algos_mapping['a_star'], 'maze4.txt')
