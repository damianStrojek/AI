from exceptions import GameplayException
import copy, time
from collections import defaultdict
from connect4 import Connect4
from agents import MinMaxAgent, AlphaBetaAgent, RandomAgent
from heuristics import simple_score, advanced_score


def mean(l):
    return sum(l) / len(l)


def single_game(agent1, agent2, do_draw=True):
    """

    :param agent1:
    :param agent2:
    :param do_draw:
    :return: returns who won, average time per move for agent1, average time per move for agent2
    """
    connect4 = Connect4(width=7, height=6)
    times = defaultdict(list)
    while not connect4.game_over:
        if do_draw:
            connect4.draw()
        try:
            t = time.time()
            if connect4.who_moves == agent1.my_token:
                n_column = agent1.decide(copy.deepcopy(connect4))
            else:
                n_column = agent2.decide(copy.deepcopy(connect4))
            times[connect4.who_moves].append(time.time() - t)
            connect4.move(n_column)
        except (ValueError, GameplayException):
            if do_draw:
                print('invalid move')
        if do_draw:
            connect4.draw()
    return connect4.wins, mean(times[agent1.my_token]), mean(times[agent2.my_token])


def compare_AIs(agent1, agent2, ntrials=10):
    outcome = {'x': 0, 'o': 0, 'draw': 0}
    avg_times = defaultdict(list)
    for n in range(ntrials):
        print(f"Game {n + 1}/{ntrials}...", end="")
        result, t1, t2 = single_game(agent1, agent2, False)
        result = 'draw' if result is None else result
        outcome[result] += 1
        avg_times[agent1.my_token].append(t1)
        avg_times[agent2.my_token].append(t2)
        print(f" done. Result: {result}, avg times: {agent1}: {t1: 0.4f}s, {agent2}: {t2: 0.4f}s")
    print(f"Results of {ntrials} games:\n {outcome}")
    avg_avg_times = {a: mean(avg_times[a]) for a in avg_times.keys()}
    print("Avg per move times:")
    for ag in [agent1, agent2]:
        print(f"\t{ag}: {avg_avg_times[ag.my_token]: 0.4f}s")
    return outcome, avg_avg_times


if __name__ == '__main__':
    agent1 = RandomAgent('o', depth=4, heuristic_fun=advanced_score)
    agent2 = AlphaBetaAgent('x', depth=4, heuristic_fun=advanced_score)

    single_game(agent1, agent2)
    # compare_AIs(agent1, agent2, 5)
