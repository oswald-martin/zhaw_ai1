from copy import deepcopy
from random import choice
from game import Board
import numpy as np

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3

MOVES = [LEFT, UP, RIGHT, DOWN]


class MCTS:
    def __init__(self, board: Board, parent=None, parent_move=None) -> None:
        self.board = board
        self.parent = parent
        self.parent_move = parent_move
        self.children = []
        self.__branch = board.branch()
        self.__nr_visits = 0
        self.__score = 0

    def q(self) -> int:
        return self.__score

    def n(self) -> int:
        return self.__nr_visits

    def __is_terminal_node__(self):
        return self.board.game_over

    def __selection__(self):
        current_node = self
        while not current_node.__is_terminal_node__():
            if not current_node.__is_fully_expandet__():
                return current_node.__expand__()
            else:
                current_node = current_node.__best_child__()
        return current_node

    def __expand__(self):
        move = choice(list(self.__branch.keys()))
        next_board = self.__branch.pop(move)
        child_node = MCTS(next_board, self, move)
        self.children.append(child_node)
        return child_node

    def __play_out__(self):
        board = deepcopy(self.board)
        while not board.game_over:
            move = choice(MOVES)
            board.make_move(move)
        return board.get_score()

    def __backpropagate__(self, score):
        self.__nr_visits += 1
        self.__score += score
        if self.parent:
            self.parent.__backpropagate__(score)

    def __is_fully_expandet__(self):
        return len(self.__branch) == 0

    def __best_child__(self, c_param=np.sqrt(2)):
        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def best_move(self, simulation_no):
        for i in range(simulation_no):
            v = self.__selection__()
            score = v.__play_out__()
            v.__backpropagate__(score)

        return self.__best_child__(c_param=0.).parent_move
