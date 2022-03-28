from connect4 import Connect4
import random

'''
    Functions here should return a scalar value of a current 'position'
    in Connect4 game as seen for player playing with 'token' (one of ['o', 'x']).
'''


def random_score(position: Connect4, token='x'):
    return random.randint(-1000, 1000)


def simple_score(position: Connect4, token='x'):
    opposite_token = 'o' if token == 'x' else 'x'
    if position.game_over:
        if position.wins == token:
            return 1000
        elif position.wins == opposite_token:
            return -1000
        else:  # tie
            return 0
    score = 0
    for four in position.iter_fours():
        if four.count(token) == 3 and four.count('_') == 1:
            score += 10
    return score


def advanced_score(position: Connect4, token='x'):
    opposite_token = 'o' if token == 'x' else 'x'
    if position.game_over:
        if position.wins == token:
            return 1000
        elif position.wins == opposite_token:
            return -1000
        else:  # tie
            return 0
    score = 0
    for four in position.iter_fours():
        if four.count(token) == 4:
            score += 50
        elif four.count(token) == 3 and four.count('_') == 1:
            score += 25
        elif four.count(token) == 2 and four.count('_') == 2:
            score += 10
        if four.count(opposite_token) == 3 and four.count('_') == 1:
            score -= 25
    return score
