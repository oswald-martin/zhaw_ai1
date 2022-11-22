from random import choice
import numpy as np
from copy import deepcopy

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
RANDOM_TILES = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]


class Game():

    def __init__(self, board=None) -> None:
        self.game_over = False
        if board is None:
            self.reset()
        else:
            self.__board = board
        self.__score = np.int64(0)
        self.__reward_diff = np.int64(0)

    def get_board(self) -> np.ndarray:
        return np.copy(self.__board)

    def get_score(self) -> np.int64:
        return self.__score

    def get_score_diff(self) -> np.int64:
        return self.__reward_diff

    def make_move(self, move, spawn_tile=True) -> None:
        tmp_board = np.rot90(self.__board, move)
        tmp_board = self.__stack__(tmp_board)
        tmp_board = self.__merge__(tmp_board)
        tmp_board = self.__stack__(tmp_board)
        tmp_board = np.rot90(tmp_board, 4-move)

        if np.array_equal(tmp_board, self.__board):
            self.game_over = True
        else:
            self.__board = tmp_board
            if spawn_tile:
                self.spawn_random_tile()

        self.__check_gameover__()

    def branch(self) -> dict:
        res = {}
        for move in range(4):
            tmp_board = deepcopy(self)
            tmp_board.make_move(move)
            res[move] = tmp_board
        return res

    def branch_all(self, n: int):
        res = []
        idx_empty_tiles = np.argwhere(board == 0)
        for idx in idx_empty_tiles:
            tmp_b = np.copy(board)
            tmp_b[idx[0], idx[1]] = n
            res.append(tmp_b)
        return res

    def reset(self) -> None:
        self.game_over = False
        self.__board = np.zeros((4, 4), dtype=np.int32)
        self.spawn_random_tile()
        self.spawn_random_tile()

    def spawn_random_tile(self, n=None) -> None:
        empty_tiles = np.argwhere(self.__board == 0)
        number = choice(RANDOM_TILES) if n is None else n
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
        if add_score:
            self.__reward_diff = 0
        for i in range(4):
            for j in range(3):
                if tmp_board[i, j] == tmp_board[i, j+1]:
                    tmp_board[i, j+1] = 0
                    tmp_board[i, j] = 2*tmp_board[i, j]
                    if add_score:
                        tmp_score = np.int64(tmp_board[i, j])
                        self.__reward_diff += tmp_score
                        self.__score += tmp_score
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


if __name__ == '__main__':
    bla = np.array([[2, 2, 0, 2], [0, 0, 0, 4], [2, 0, 0, 8], [0, 0, 0, 8]])
    board = Game(bla)
    board.make_move(DOWN)
    print(board.get_score_diff())
    board.make_move(LEFT)
    print(board.get_score_diff())
    print(board.game_over)
