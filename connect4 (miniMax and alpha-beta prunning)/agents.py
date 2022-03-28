import math
import sys
from abc import ABC, abstractmethod
from copy import deepcopy

from exceptions import AgentException
from heuristics import *


class Agent(ABC):
    def __init__(self, my_token='o', **kwargs):
        self.my_token = my_token

    @abstractmethod
    def decide(self, connect4):
        pass

    def __str__(self):
        return f"{self.my_token} ({self.__class__.__name__})"


class RandomAgent(Agent):
    def __init__(self, my_token='o', **kwargs):
        super().__init__(my_token, **kwargs)

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')
        return random.choice(connect4.possible_moves())


class MinMaxAgent(Agent):
    def __init__(self, my_token='o', depth=4, heuristic_fun=random_score):
        super().__init__(my_token)
        self.depth = depth
        self.heuristic_fun = heuristic_fun

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        best_move, best_score = self.minmax(connect4, depth=self.depth)
        return best_move

    def minmax(self, connect4: Connect4, depth=4, maximizing=True):
        possible_moves = connect4.possible_moves()
        if connect4.game_over or depth == 0:
            return None, self.heuristic_fun(connect4, self.my_token)
        if maximizing:
            value = -math.inf
            column = random.choice(possible_moves)
            for child in possible_moves:
                new_board = deepcopy(connect4)
                new_board.move(child)
                # next invoke is minimizing
                new_value = self.minmax(new_board, depth-1, False)[1]
                if new_value > value:
                    value = new_value
                    column = child
            return column, value
        else:
            value = +math.inf
            column = random.choice(possible_moves)
            for child in possible_moves:
                new_board = deepcopy(connect4)
                new_board.move(child)
                new_value = self.minmax(new_board, depth-1, True)[1]
                if new_value < value:
                    value = new_value
                    column = child
            return column, value


class AlphaBetaAgent(Agent):
    def __init__(self, my_token='o', depth=4, heuristic_fun=random_score):
        super().__init__(my_token)
        self.depth = depth
        self.heuristic_fun = heuristic_fun

    def decide(self, connect4):
        if connect4.who_moves != self.my_token:
            raise AgentException('not my round')

        best_move, best_score = self.alpha_beta(connect4, depth=self.depth)
        return best_move

    def alpha_beta(self, connect4: Connect4, depth=4, maximizing=True, alpha=-sys.maxsize, beta=sys.maxsize):
        possible_moves = connect4.possible_moves()
        if connect4.game_over or depth == 0:
            return None, self.heuristic_fun(connect4, self.my_token)
        if maximizing:
            value = -math.inf
            column = random.choice(possible_moves)
            for child in possible_moves:
                new_board = deepcopy(connect4)
                new_board.move(child)
                new_value = self.alpha_beta(new_board, depth - 1, False, alpha, beta)[1]
                if new_value > value:
                    value = new_value
                    column = child
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return column, value
        else:
            value = +math.inf
            column = random.choice(possible_moves)
            for child in possible_moves:
                new_board = deepcopy(connect4)
                new_board.move(child)
                new_value = self.alpha_beta(new_board, depth - 1, True, alpha, beta)[1]
                if new_value < value:
                    value = new_value
                    column = child
                if value <= alpha:
                    break
                beta = min(beta, value)
            return column, value

