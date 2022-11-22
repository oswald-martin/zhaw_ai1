from py_game import Game
import numpy as np

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
MOVES = [LEFT, UP, RIGHT, DOWN]


class Node:
    def __init__(self, board, max_depth=3, parent=None, parent_move=None, chance_node=None, heuristic=None) -> None:
        self.game = Game(board)
        self.parent = parent
        self.parent_move = parent_move
        self.children = []
        self.__heurisic = heuristic
        self.__depth = max_depth
        self.__chance_node = chance_node
        self.__expectimax_val = 0

    def is_terminal_node(self):
        return self.game.game_over

    def heuristic_val(self):
        return self.__heurisic.eval(self.game.get_board())

    def __expand__(self):
        board = self.game.get_board()
        if self.is_terminal_node():
            return
        for move in MOVES:
            node = Node(board, self.__depth-1, self, move, True, self.__heurisic)
            node.game.make_move(move, False)
            self.children.append(node)

    def expectimax(self):
        if self.is_terminal_node() or self.__depth == 0:
            return self.heuristic_val()
        if self.__chance_node:
            alpha = 0
            b2 = self.game.branch_all(2)
            b4 = self.game.branch_all(4)
            nr_nodes = len(b2) + len(b4)
            for b in b2:
                node = Node(b, self.__depth-1, self, None, False, self.__heurisic)
                alpha += 0.9 * node.expectimax() / nr_nodes
            for b in b4:
                node = Node(b, self.__depth-1, self, None, False, self.__heurisic)
                alpha += 0.1 * node.expectimax() / nr_nodes
            self.__expectimax_val = alpha
            return alpha
        else:
            self.__expand__()
            alpha = -np.inf
            for child in self.children:
                alpha = max(alpha, child.expectimax())
            self.__expectimax_val = alpha
            return alpha

    def best_move(self):
        self.__expand__()
        best = self.children[0]
        for child in self.children:
            child.expectimax()
            if child.__expectimax_val > best.__expectimax_val:
                best = child
        return best.parent_move
