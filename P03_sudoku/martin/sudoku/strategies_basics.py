from sudoku import Sudoku, get_sample_sudoku
from itertools import combinations
from auxillary_funcs import filter_solved_cells


########################################################################################################################
# Naked singles to quads
########################################################################################################################

def __apply_naked_n_col__(sudoku: Sudoku, n):
    rem = False
    for col in sudoku.getall_cols():
        col = filter_solved_cells(col) if n != 1 else col
        for comb in combinations(col, n):
            union = set().union(*[s[1] for s in comb])
            if len(union) == n:
                ex_idx = [i[0] for i in comb]
                for val in union:
                    rem = sudoku.rem_col(ex_idx, val, ex_idx) or rem
    return rem


def __apply_naked_n_row__(sudoku: Sudoku, n):
    rem = False
    for row in sudoku.getall_rows():
        row = filter_solved_cells(row) if n != 1 else row
        for comb in combinations(row, n):
            union = set().union(*[s[1] for s in comb])
            if len(union) == n:
                ex_idx = [i[0] for i in comb]
                for val in union:
                    rem = sudoku.rem_row(ex_idx, val, ex=ex_idx) or rem
    return rem


def __apply_naked_n_sqr__(sudoku: Sudoku, n):
    rem = False
    for sqr in sudoku.getall_sqrs():
        sqr = filter_solved_cells(sqr) if n != 1 else sqr
        for comb in combinations(sqr, n):
            union = set().union(*[s[1] for s in comb])
            if len(union) == n:
                ex_idx = [i[0] for i in comb]
                for val in union:
                    rem = sudoku.rem_sqr(ex_idx, val, ex=ex_idx) or rem
    return rem


def apply_naked_n(sudoku: Sudoku, v=None):
    if sudoku.is_solved():
        return
    rem = False
    n = 1
    while n <= 4:
        elim = False
        elim = __apply_naked_n_col__(sudoku, n) or elim
        elim = __apply_naked_n_row__(sudoku, n) or elim
        elim = __apply_naked_n_sqr__(sudoku, n) or elim
        if v is not None:
            print(sudoku)
        n = 1 if elim else n+1
        rem = rem or elim
    return rem


########################################################################################################################
# Hidden singles to quads
########################################################################################################################


def __apply_hidden_n_col__(sudoku: Sudoku, n):
    rem = False
    for col in sudoku.getall_cols():
        for comb in combinations(range(9), n):
            cells = set().union(*[col[i][1] for i in comb])
            rest = set().union(*[col[i][1] for i in range(9) if i not in comb])
            diff = cells.difference(rest)
            if len(diff) == n:
                rem_cells = [col[i][0] for i in comb]
                for val in rest:
                    rem = sudoku.rem_cels(rem_cells, val) or rem
    return rem


def __apply_hidden_n_row__(sudoku: Sudoku, n):
    rem = False
    for row in sudoku.getall_rows():
        for comb in combinations(range(9), n):
            cells = set().union(*[row[i][1] for i in comb])
            rest = set().union(*[row[i][1] for i in range(9) if i not in comb])
            diff = cells.difference(rest)
            if len(diff) == n:
                rem_cells = [row[i][0] for i in comb]
                for val in rest:
                    rem = sudoku.rem_cels(rem_cells, val) or rem
    return rem


def __apply_hidden_n_sqr__(sudoku: Sudoku, n):
    rem = False
    for sqr in sudoku.getall_sqrs():
        for comb in combinations(range(9), n):
            cells = set().union(*[sqr[i][1] for i in comb])
            rest = set().union(*[sqr[i][1] for i in range(9) if i not in comb])
            diff = cells.difference(rest)
            if len(diff) == n:
                rem_cells = [sqr[i][0] for i in comb]
                for val in rest:
                    rem = sudoku.rem_cels(rem_cells, val) or rem
    return rem


def apply_hidden_n(sudoku: Sudoku, v=None):
    if sudoku.is_solved():
        return
    rem = False
    n = 1
    while n <= 4:
        elim = False
        elim = __apply_hidden_n_col__(sudoku, n) or elim
        elim = __apply_hidden_n_row__(sudoku, n) or elim
        elim = __apply_hidden_n_sqr__(sudoku, n) or elim
        if v is not None:
            print(sudoku)
        n = 1 if elim else n+1
        rem = rem or elim
    return rem


########################################################################################################################
# Apply basic strategies
########################################################################################################################

def apply_basic_strategies(sudoku: Sudoku, v=None):
    if sudoku.is_solved():
        return
    elim = True
    rem = False
    while elim:
        elim = False
        elim = apply_naked_n(sudoku, v) or elim
        elim = apply_hidden_n(sudoku, v) or elim
        rem = rem or elim
    return rem


if __name__ == '__main__':
    sudoku = get_sample_sudoku()
    apply_basic_strategies(sudoku)
    print(sudoku)
