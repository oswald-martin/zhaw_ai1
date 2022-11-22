import numpy as np
from math import floor
from prettytable import PrettyTable, ALL
from copy import deepcopy


class IllegalMove(Exception):
    def __init__(self, message):
        super().__init__(message)


class Sudoku():

    def __init__(self, board) -> None:
        self._board = np.array([{1, 2, 3, 4, 5, 6, 7, 8, 9} for _ in range(81)]).reshape((9, 9))
        # set board vals
        for idx in zip(*np.nonzero(board)):
            val = board[idx[0]][idx[1]]
            self.set_val(idx, val)

    def getall_rows(self):
        return [self.get_row((i, 0)) for i in range(9)]

    def getall_cols(self):
        return [self.get_col((0, i)) for i in range(9)]

    def getall_sqrs(self):
        return [self.get_sqr((3*i, 3*j)) for i in range(3) for j in range(3)]

    def get_cel(self, idx):
        r, c = idx
        cell = deepcopy(self._board[r][c])
        return (idx, cell)

    def get_row(self, idx):
        return [self.get_cel((idx[0], i)) for i in range(9)]

    def get_col(self, idx):
        return [self.get_cel((i, idx[1])) for i in range(9)]

    def get_sqr(self, idx):
        r = floor(idx[0]/3)*3
        c = floor(idx[1]/3)*3
        return [self.get_cel((r+i, c+j)) for i in range(3) for j in range(3)]

    def rem_cel(self, idx, val):
        rem = False
        r, c = idx
        s = self._board[r][c]
        if val in s:
            if len(s) == 1:
                print(self)
                raise IllegalMove(f'val {val} can not be removed from idx {idx}')
            rem = True
            s.remove(val)
        return rem

    def rem_cels(self, idx_lst, val):
        rem = False
        for index in idx_lst:
            r, c = index
            rem = self.rem_cel((r, c), val) or rem
        return rem

    def rem_row(self, idx_lst, val, ex=[]):
        rem = False
        for index in idx_lst:
            r, c = index
            for i in range(9):
                if (r, i) not in ex:
                    rem = self.rem_cel((r, i), val) or rem
        return rem

    def rem_col(self, idx_lst, val, ex=[]):
        rem = False
        for index in idx_lst:
            r, c = index
            for i in range(9):
                if (i, c) not in ex:
                    rem = self.rem_cel((i, c), val) or rem
        return rem

    def rem_sqr(self, idx, val, ex=[]):
        rem = False
        for index in idx:
            r = floor(index[0]/3)*3
            c = floor(index[1]/3)*3
            for i in range(r, r+3, 1):
                for j in range(c, c+3, 1):
                    if (i, j) not in ex:
                        rem = self.rem_cel((i, j), val) or rem
        return rem

    def rem_all(self, idx, val, ex=[]):
        rem = False
        rem = self.rem_col(idx, val, ex) or rem
        rem = self.rem_row(idx, val, ex) or rem
        rem = self.rem_sqr(idx, val, ex) or rem
        return rem

    def set_val(self, idx, val):
        if self.is_legal(idx, val):
            r, c = idx
            self.rem_all([idx], val)
            self._board[r][c] = {val}
        else:
            print(self)
            raise IllegalMove(f'val {val} can not be placed on idx {idx}')

    def is_legal(self, idx, val):
        r, c = idx
        return val in self._board[r][c]

    def is_solved(self):
        for i in range(9):
            for j in range(9):
                if len(self._board[j][i]) != 1:
                    return False
        return True

    def __str__(self) -> str:
        tab = PrettyTable()
        tab.hrules = ALL
        tab.hrules = ALL
        tab.max_width = {}
        for i in range(1, 10, 1):
            tab.max_width[f'Field {i}'] = 8
        tab.add_rows(self._board)
        tabstr = tab.get_string().split('\n')
        return '\n'.join(tabstr[2:]) + '\n'


def get_sample_sudoku():
    board = [[0, 0, 0, 2, 0, 0, 0, 6, 3],
             [3, 0, 0, 0, 0, 5, 4, 0, 1],
             [0, 0, 1, 0, 0, 3, 9, 8, 0],
             [0, 0, 0, 0, 0, 0, 0, 9, 0],
             [0, 0, 0, 5, 3, 8, 0, 0, 0],
             [0, 3, 0, 0, 0, 0, 0, 0, 0],
             [0, 2, 6, 3, 0, 0, 5, 0, 0],
             [5, 0, 3, 7, 0, 0, 0, 0, 8],
             [4, 7, 0, 0, 0, 1, 0, 0, 0]]
    return Sudoku(board)


if __name__ == '__main__':
    sudoku = get_sample_sudoku()
    print(sudoku)
    print(sudoku.is_solved())
