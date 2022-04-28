import os
import analyse
from checker import checker
from datetime import datetime


def cross(A, B, c=''):

    return [a + b + c for a in A for b in B]


besli_thread_karesi = []
besli_thread_zamani = []

onlu_thread_karesi = []
onlu_thread_zamani = []

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits

id_var = 'a'  # top left
sol_ust_kare = cross(rows, cols, id_var)
unitlist_a = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'b'  # top right
sag_ust_kare = cross(rows, cols, id_var)
unitlist_b = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'c'  # bottom left
sol_alt_kare = cross(rows, cols, id_var)
unitlist_c = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'd'  # bottom right
sag_alt_kare = cross(rows, cols, id_var)
unitlist_d = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])


def repl(c):
    a = b = 0
    s = ""
    if c[0] in 'ABCGHI' and c[1] in '123789':
        if c[0] in 'ABC':
            s += chr(ord(c[0]) + 6)
            a = 1
        elif c[0] in 'GHI':
            s += chr(ord(c[0]) - 6)
            a = 2
        if c[1] in '123':
            s += chr(ord(c[1]) + 6)
            b = 1
        elif c[1] in '789':
            s += chr(ord(c[1]) - 6)
            b = 2
    else:
        return c
    if a == 1 and b == 1:
        s += 'a'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s


id_var = '+'
ortanca_kare = [repl(x) for x in cross(rows, cols, id_var)]
unitlist_mid = ([ortanca_kare[x * 9:x * 9 + 9] for x in range(0, 9)] +
                [ortanca_kare[x::9] for x in range(0, 9)] +
                [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
                 for cs in ('123', '456', '789')
                 if not (rs in 'ABCGHI' and cs in '123789')])

tum_kareler = set(sol_ust_kare + sag_ust_kare + sol_alt_kare + sag_alt_kare + ortanca_kare)
tum_listeler = unitlist_a + unitlist_b + unitlist_c + unitlist_d + unitlist_mid

units = dict((s, [u for u in tum_listeler if s in u])
             for s in tum_kareler)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in tum_kareler)




def parse_grid_samurai(grid):

    values = dict((s, digits) for s in tum_kareler)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):

            return False
    return values


def flatten(arr):
    return [x for sub in arr for x in sub]


def grid_values(grid):

    a = flatten([x[:9] for x in grid[:9]])
    b = flatten([x[12:] for x in grid[:9]])
    c = flatten([x[:9] for x in grid[12:]])
    d = flatten([x[12:] for x in grid[12:]])
    mid = flatten([x[6:15] for x in grid[6:15]])
    chars = a + b + c + d + mid
    sqrs = sol_ust_kare + sag_ust_kare + sol_alt_kare + sag_alt_kare + ortanca_kare
    assert len(chars) == 405
    return dict(zip(sqrs, chars))





def assign(values, s, d):

    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):

    if d not in values[s]:

        return values
    values[s] = values[s].replace(d, '')

    if len(values[s]) == 0:

        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False

    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:

            return False
        elif len(dplaces) == 1:

            if not assign(values, dplaces[0], d):
                return False
    return values





def display(values, sqr):

    width = 1 + max(len(values[s]) for s in sqr)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[sqr[(ord(r) - 65) * 9 + int(c) - 1]]
                      .center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    print()


def display_samurai(vals):

    if not vals:
        print("Solution not found, please check if test is valid.")
        return
    print("Sol Üst:")
    display(vals, sol_ust_kare)
    print("Sağ Üst:")
    display(vals, sag_ust_kare)
    print("Sol Alt:")
    display(vals, sol_alt_kare)
    print("Sağ Alt:")
    display(vals, sag_alt_kare)
    print("Ortanca:")
    display(vals, ortanca_kare)


    checker(vals, [sol_ust_kare, sag_ust_kare, sol_alt_kare, sag_alt_kare, ortanca_kare])




def solve(grid, threadType):
    if threadType == 0:
        time.sleep(1)
        return search(parse_grid_samurai(grid), threadType)
    else:
        return search(parse_grid_samurai(grid), threadType)


def search(values, threadType):

    if threadType == 0:
        if values is False:
            return False

        for idx, s in enumerate(tum_kareler):
            if len(values[s]) == 1:
                besli_thread_karesi.append(idx)
                besli_thread_zamani.append((datetime.now() - analyse.besli_thread).microseconds)
                if idx == len(tum_kareler) - 1:
                    return values
            else:
                break


        n, s = min((len(values[s]), s) for s in tum_kareler if len(values[s]) > 1)
        return some(search(assign(values.copy(), s, d))
                    for d in values[s])
    else:
        if values is False:
            return False

        for idx, s in enumerate(tum_kareler):
            if len(values[s]) == 1:
                onlu_thread_karesi.append(idx)
                onlu_thread_zamani.append((datetime.now() - analyse.besli_thread).microseconds)
                if idx == len(tum_kareler) - 1:
                    return values
            else:
                break


        n, s = min((len(values[s]), s) for s in tum_kareler if len(values[s]) > 1)
        return some(search(assign(values.copy(), s, d))
                    for d in values[s])




def some(seq):

    for e in seq:
        if e: return e
    return False


def from_file(filename, sep='\n'):

    return open(filename, 'r').read().strip().split(sep)


def shuffled(seq):

    seq = list(seq)
    random.shuffle(seq)
    return seq


import time, random


def solve_all(grids, name='', showif=0.0):


    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock() - start

        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])



def solved(values):

    def unitsolved(unit):
        return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in tum_listeler)

