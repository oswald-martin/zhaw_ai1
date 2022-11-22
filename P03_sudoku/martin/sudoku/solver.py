from strategies_basics import apply_basic_strategies
from strategies_intersectionremoval import apply_intersectionremoval_strategies
from sudoku import get_sample_sudoku

sudoku = get_sample_sudoku()
v = True

elim = True
while elim:
    elim = False
    elim = apply_basic_strategies(sudoku, v) or elim
    elim = apply_intersectionremoval_strategies(sudoku, v) or elim

print(sudoku)
print(sudoku.is_solved())
