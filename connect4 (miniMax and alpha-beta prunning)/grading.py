from agents import MinMaxAgent, AlphaBetaAgent, RandomAgent
from heuristics import simple_score, advanced_score
from ava import compare_AIs


def print_info(points_to_get, condition):
    if condition:
        print(f"OK. Enough for {points_to_get} points! :)")
    else:
        print(f"Not enough for {points_to_get} points. :(")


def for_3_points():
    agent1 = RandomAgent('o')
    agent2 = MinMaxAgent('x', depth=4, heuristic_fun=simple_score)
    results, times = compare_AIs(agent1, agent2, 5)
    print_info(3, results['x'] >= 4*results['o'])


def for_4_points():
    agent1 = MinMaxAgent('o', depth=4, heuristic_fun=simple_score)
    agent2 = MinMaxAgent('x', depth=4, heuristic_fun=advanced_score)
    results, times = compare_AIs(agent1, agent2, 5)
    print_info(4, results['x'] >= 4*results['o'])


def for_5_points():
    agent1 = MinMaxAgent('o', depth=4, heuristic_fun=simple_score)
    agent2 = AlphaBetaAgent('x', depth=4, heuristic_fun=advanced_score)
    results, times = compare_AIs(agent1, agent2, 5)
    print_info(5, results['x'] >= 4*results['o'] and 4*times['x'] < times['o'])


if __name__ == '__main__':
    # for_3_points()
    # for_4_points()
    for_5_points()
