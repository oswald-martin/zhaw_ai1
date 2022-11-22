from collections import Counter, defaultdict


def filter_solved_cells(lst):
    return list(filter(lambda c: len(c[1]) != 1, lst))


def frequency_vals(lst):
    count = Counter()
    for _, s in lst:
        count.update(s)
    return count


def reverse_index(lst):
    res = defaultdict(lambda: set())
    for idx, s in lst:
        for val in s:
            res[val].add(idx)
    return res
