import random
import game
import sys
import numpy as np

# Author:				chrn (original by nneonneo)
# Date:				    11.11.2016
# Description:			The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def find_best_move(board):
    bestmove = -1

    # TODO:
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.
    bestmove = find_best_move_random_agent()
    return bestmove


def eval_board(board):
    # count empty fields
    empty_fields = board.flatten().count_nonzero(board == 0)

    # desirable positions
    desirability_matrix = np.array([[3, 2, 3, 3],
                                    [2, 1, 1, 2],
                                    [2, 1, 1, 2],
                                    [3, 2, 2, 3]], dtype=np.float64)
    desirable_positions = np.multiply(board, desirability_matrix).flatten().sum()

    # neighbour score
    neighbour_score = 0
    for i in range(3):
        for j in range(3):
            if board[i, j] == board[i+1, j]:
                neighbour_score += board[i, j]
            if board[i, j] == board[i, j+1]:
                neighbour_score += board[i, j]

    # weight scores and return
    EMPTY_FIELDS = 3
    DESIRABLE = 1
    NEIGHBOUR = 2

    return EMPTY_FIELDS*empty_fields + DESIRABLE*desirable_positions + NEIGHBOUR*neighbour_score


def find_best_move_random_agent():
    return random.choice([UP, DOWN, LEFT, RIGHT])


def execute_move(move, board):
    """
    move and return the grid without a new random tile
        It won't affect the state of the game in the browser.
    """

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")


def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return (newboard == board).all()