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
    moves = [UP,RIGHT,DOWN,LEFT]
    movesres = simBoards(board)

    scores = [eval_board(np.array(moveres)) for moveres in movesres]

    best = np.argmax(scores)
    # TODO:
    # Build a heuristic agent on your own that is much better than the random agent.
    # Your own agent don't have to beat the game.
    bestmove = moves[best]
    return bestmove


def eval_board(board):

    if np.array_equal(board,np.array(None)):return 0
    # count empty fields
    empty_fields = np.count_nonzero(board.flatten() == 0)

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
    EMPTY_FIELDS = 100
    DESIRABLE = 1
    NEIGHBOUR = 0

    return EMPTY_FIELDS*empty_fields + DESIRABLE*desirable_positions + NEIGHBOUR*neighbour_score


def simulate_spawn_tile(board):
    res = []
    idx_empty_tiles = np.argwhere(board == 0)
    for idx in idx_empty_tiles:
        tmp_2 = np.copy(board)
        tmp_4 = np.copy(board)
        tmp_2[idx[0], idx[1]] = 2
        tmp_4[idx[0], idx[1]] = 4
        res.append(tmp_2)
        res.append(tmp_4)
    return res


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


def simBoards(board):
    '''
    takes board as input and simulates the 4 moves(without the random item added)
    returns: up,right,down,left ->clockwise
    '''
    right = board
    down = np.rot90(board, 1)
    left = np.rot90(board, 2)
    up = np.rot90(board, 3)

    right = MoveSim(right)
    down = MoveSim(down)
    left = MoveSim(left)
    up = MoveSim(up)

<<<<<<< HEAD
    down = np.rot90(down,3)
    left = np.rot90(left,2)
    up = np.rot90(up,1)

    if np.array_equal(board,up):    up = None
    if np.array_equal(board,right): right = None
    if np.array_equal(board,down):  down = None
    if np.array_equal(board,left):  left = None

    return up,right,down,left
=======
    down = np.rot90(down, 3)
    left = np.rot90(left, 2)
    up = np.rot90(up, 1)
    return up, right, down, left
>>>>>>> 80e0fb78ec9a73698d73e6eebba2f72c3c659fa9


def MoveSim(board):
    board = np.array(board)
    newboard = np.zeros_like(board)
    for j in range(len(board)):
        line = board[j]
        line = line[line != 0]
        i = 1

        while i < len(line):

            if line[-i] == line[-i-1]:
                line[-i] *= 2
                line = np.delete(line, -i-1)
                i += 1
            i += 1

        zeroes = [0] * (4-len(line))

        newLine = np.concatenate((zeroes, line))
        newboard[j] = newLine

    return newboard
