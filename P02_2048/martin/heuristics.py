import numpy as np
from py_game import Game

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
MOVES = [LEFT, UP, RIGHT, DOWN]


class Heuristic():

    def __init__(self, empty_weight, edge_weight, mon_weight, max_weight, score_weight) -> None:
        self._w_emp = empty_weight
        self._w_edg = edge_weight
        self._w_mon = mon_weight
        self._w_max = max_weight
        self._w_sco = score_weight

    def branch_eval(self, board: np.ndarray) -> np.ndarray:
        scores = np.ones(4)
        for m in range(4):
            g = Game(board)
            g.make_move(m)
            if g.game_over:
                continue
            score = self.eval(g.get_board())
            scores[m] = score
        return scores / scores.sum()

    def eval(self, board: np.ndarray) -> float:
        g = Game(board)
        b = g.get_board()
        emp = self.__empty_tiles__(b)
        edg = self.__max_value_edge__(b)
        mon = self.__monoticity__(b)
        ma = board.max()
        sco = g.get_score_diff()
        return emp*self._w_emp + edg*self._w_edg + mon*self._w_mon*ma + ma*self._w_max + sco*self._w_sco

    def __empty_tiles__(self, board: np.ndarray):
        return np.count_nonzero(board.flatten() == 0)

    def __max_value_edge__(self, board: np.ndarray):
        corners = np.array([[0, 0], [3, 0], [0, 3], [3, 3]])
        max_tiles = np.where(board == np.amax(board))
        for pos in max_tiles:
            if pos in corners:
                return 1.0
        return 0.

    def __monoticity__(self, board: np.ndarray):
        h1 = np.where(np.arange(4)[:, None] % 2, board[:, ::-1], board).ravel().flatten()
        v1 = np.where(np.arange(4)[:, None] % 2, np.rot90(board, -1)[:, ::-1], np.rot90(board, -1)).ravel().flatten()
        h2 = np.where(np.arange(4)[:, None] % 2, np.rot90(board, 2)[:, ::-1], np.rot90(board, 2)).ravel().flatten()
        v2 = np.where(np.arange(4)[:, None] % 2, np.rot90(board, 1)[:, ::-1], np.rot90(board, 1)).ravel().flatten()
        h1_mon = 1.0 if all(x >= y for x, y in zip(h1, h1[1:])) or all(x <= y for x, y in zip(h1, h1[1:])) else 0.
        v1_mon = 1.0 if all(x >= y for x, y in zip(v1, v1[1:])) or all(x <= y for x, y in zip(v1, v1[1:])) else 0.
        h2_mon = 1.0 if all(x >= y for x, y in zip(h2, h2[1:])) or all(x <= y for x, y in zip(h2, h2[1:])) else 0.
        v2_mon = 1.0 if all(x >= y for x, y in zip(v2, v2[1:])) or all(x <= y for x, y in zip(v2, v2[1:])) else 0.
        return h1_mon + h2_mon + v1_mon + v2_mon
