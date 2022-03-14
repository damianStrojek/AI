from maze import Maze, NodeType


def bfs(maze):
    start_node = maze.find_node(NodeType.START)
    q = [start_node]
    counter = 0
    while len(q) > 0:
        counter += 1
        node = q.pop(0)  # FIFO
        node.visited = True
        if node.type == NodeType.GOAL:
            return Maze.path_from(node), counter

        for child in maze.get_possible_movements(node):
            if not child.visited and child.parent is None:
                child.parent = node
                q.append(child)

        maze.draw()

    return None, counter


def dfs(maze):
    start_node = maze.find_node(NodeType.START)
    q = [start_node]
    counter = 0
    while len(q) > 0:
        counter += 1
        node = q.pop()
        node.visited = True
        if node.type == NodeType.GOAL:
            return Maze.path_from(node), counter

        for child in maze.get_possible_movements(node):
            if not child.visited and child.parent is None:
                child.parent = node
                q.append(child)

        maze.draw()

    return None, counter


def dijkstra(maze):
    raise NotImplementedError()  # TODO


def a_star(maze):
    startNode = maze.find_node(NodeType.START)
    openList = [startNode]
    gScore = {startNode: 0}  # function g
    fScore = {startNode: heuristic_cost(maze, startNode)}  # function f
    counter = 0

    while openList:
        counter += 1
        current = None
        minScore = None

        for i in openList:
            if minScore is None or fScore[i] < minScore:
                minScore = fScore[i]
                current = i
        if current.type == NodeType.GOAL:
            startNode.parent = None
            return Maze.path_from(current), counter
        openList.remove(current)
        current.visited = True

        for children in maze.get_possible_movements(current):
            if children.visited:
                continue
            # Distance is a distance from start to the children through current
            distance = gScore[current] + maze.move_cost(children)
            if not gScore.get(children) or distance < gScore[children]:
                children.parent = current
                gScore[children] = distance
                fScore[children] = distance + heuristic_cost(maze, children)

                if children not in openList:
                    openList.append(children)
                if children.type == NodeType.GOAL:
                    startNode.parent = None
                    return Maze.path_from(children), counter+1
        maze.draw()
    startNode.parent = None
    return None, counter


def heuristic_cost(maze, node):
    end_node = maze.find_node(NodeType.GOAL)
    # cost = self.move_cost(node) - self.move_cost(self.find_node(NodeType.GOAL))
    return abs(node.x - end_node.x) + abs(node.y - end_node.y)


algos_mapping = {'a_star': a_star, 'bfs': bfs, 'dfs': dfs, 'dijkstra': dijkstra}
