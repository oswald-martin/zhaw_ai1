from random import choice
import numpy as np
from copy import deepcopy

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
RANDOM_TILES = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]


class Board():

    def __init__(self, board=None) -> None:
        self.game_over = False
        if board is None:
            self.__board = np.zeros((4, 4), dtype=np.int16)
            self.__spawn_random_tile__()
            self.__spawn_random_tile__()
        else:
            self.__board = board
        self.__score = 0

    def get_board(self) -> np.ndarray:
        return np.copy(self.__board)

    def get_score(self) -> int:
        return self.__score

    def make_move(self, move) -> None:
        tmp_board = np.rot90(self.__board, move)
        tmp_board = self.__stack__(tmp_board)
        tmp_board = self.__merge__(tmp_board)
        tmp_board = self.__stack__(tmp_board)
        tmp_board = np.rot90(tmp_board, 4-move)

        if np.array_equal(tmp_board, self.__board):
            self.game_over = True
        else:
            self.__board = tmp_board
            self.__spawn_random_tile__()

        self.__check_gameover__()

    def branch(self) -> dict:
        res = {}
        for move in range(4):
            tmp_board = deepcopy(self)
            tmp_board.make_move(move)
            res[move] = tmp_board
        return res

    def __spawn_random_tile__(self) -> None:
        empty_tiles = np.argwhere(self.__board == 0)
        number = choice(RANDOM_TILES)
        idy, idx = choice(empty_tiles)
        self.__board[idy, idx] = number

    def __stack__(self, board):
        tmp_board = np.zeros_like(board)
        for i in range(4):
            row = board[i]
            row = row[row != 0]
            tmp_board[i, :len(row)] = row
        return tmp_board

    def __merge__(self, board, add_score=True):
        tmp_board = np.copy(board)
        for i in range(4):
            for j in range(3):
                if tmp_board[i, j] == tmp_board[i, j+1]:
                    tmp_board[i, j+1] = 0
                    tmp_board[i, j] = 2*tmp_board[i, j]
                    if add_score:
                        self.__score += tmp_board[i, j]
        return tmp_board

    def __check_gameover__(self):
        for move in range(4):
            tmp_board = np.rot90(self.__board, move)
            tmp_board = self.__stack__(tmp_board)
            tmp_board = self.__merge__(tmp_board, False)
            tmp_board = self.__stack__(tmp_board)
            tmp_board = np.rot90(tmp_board, 4-move)
            if not np.array_equal(tmp_board, self.__board):
                return
        self.game_over = True
