from sudoku import Sudoku, get_sample_sudoku
from itertools import combinations
from auxillary_funcs import filter_solved_cells, reverse_index


########################################################################################################################
# Pointing Pairs and Triples
########################################################################################################################

def apply_pointing(sudoku: Sudoku, v=None):
    rem = False
    for sqr in sudoku.getall_sqrs():
        sqr = filter_solved_cells(sqr)
        rev_idx = reverse_index(sqr)
        for val, idxs in rev_idx.items():
            idxs = list(idxs)
            is_row = all(idx[0] == idxs[0][0] for idx in idxs)
            is_col = all(idx[1] == idxs[0][1] for idx in idxs)
            if is_row:
                sudoku.rem_row(idxs, val, idxs) or rem
            elif is_col:
                sudoku.rem_col(idxs, val, idxs) or rem
    if v is not None:
        print(sudoku)
    return rem


########################################################################################################################
# Line-Box Reduction
########################################################################################################################

def apply_linebox(sudoku: Sudoku, v=None):
    rem = False
    for sqr in sudoku.getall_sqrs():
        sqr = filter_solved_cells(sqr)
        rev_idx = reverse_index(sqr)
        for val, idxs in rev_idx.items():
            idxs = list(idxs)
            is_row = all(idx[0] == idxs[0][0] for idx in idxs)
            is_col = all(idx[1] == idxs[0][1] for idx in idxs)
            if is_row:
                row = sudoku.get_row(idxs[0])
                outside_sqr = set().union(*[s[1] for s in row if s[0] not in idxs])
                if {val}.isdisjoint(outside_sqr):
                    sudoku.rem_sqr(idxs, val, idxs)
            elif is_col:
                col = sudoku.get_col(idxs[0])
                outside_sqr = set().union(*[s[1] for s in col if s[0] not in idxs])
                if {val}.isdisjoint(outside_sqr):
                    sudoku.rem_sqr(idxs, val, idxs)
    if v is not None:
        print(sudoku)
    return rem


########################################################################################################################
# Apply Intersection Removal
########################################################################################################################

def apply_intersectionremoval_strategies(sudoku: Sudoku, v=None):
    if sudoku.is_solved():
        return
    elim = True
    rem = False
    while elim:
        elim = False
        elim = apply_pointing(sudoku, v) or elim
        elim = apply_linebox(sudoku, v) or elim
        rem = rem or elim
    return rem


if __name__ == '__main__':
    sudoku = get_sample_sudoku()
    apply_intersectionremoval_strategies(sudoku)
    print(sudoku)
