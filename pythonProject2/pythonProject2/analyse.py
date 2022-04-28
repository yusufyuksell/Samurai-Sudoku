import samurai
import math
import csv
import signal
import time
from datetime import datetime
import threading
from matplotlib import pyplot as plt
from sudoku import *
from collections import Counter


besli_thread = datetime.now()
onlu_thread = datetime.now()

square_indices_map = {}
index_squares_map = {}



def cross(A, B, c=''):

    return [a + b + c for a in A for b in B]

satirlar = 'ABCDEFGHI'
rakamlar = '123456789'
cols = rakamlar

id_var = 'sol_ust'
sol_ust_kare = cross(satirlar, cols, id_var)
unitlist_a = ([cross(satirlar, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in satirlar] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'sag_ust'
sag_ust_kare = cross(satirlar, cols, id_var)
unitlist_b = ([cross(satirlar, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in satirlar] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'sol_alt'
sol_alt_kare = cross(satirlar, cols, id_var)
unitlist_c = ([cross(satirlar, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in satirlar] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'sag_alt'
sag_alt_kare = cross(satirlar, cols, id_var)
unitlist_d = ([cross(satirlar, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in satirlar] +
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
        s += 'sol_ust'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s



def index_to_square(index):
    if index not in index_squares_map:
        index_squares_map[index] = chr(math.floor(index / 9) + ord('A')) + str(index % 9 + 1)
    return index_squares_map[index]


def count_initialized_squares(grid, count_map):
    for i in range(len(grid)):
        if grid[i] != '.':
            count_map[index_to_square(i)] += 1
    return count_map




def veritabanina_yaz(name, counter):
    writer = csv.writer(open(name, 'w'))
    writer.writerow(['Y-Axis', 'X-Axis', 'Number of Hits'])
    for key, value in counter.items():
        writer.writerow([key[0], key[1], value])



sol_ust = Counter()
sag_ust = Counter()
sol_alt = Counter()
sag_alt = Counter()
orta = Counter()


id_var = 'orta'
ortanca_kare = [repl(x) for x in cross(satirlar, cols, id_var)]
ortanca_liste = ([ortanca_kare[x * 9:x * 9 + 9] for x in range(0, 9)] +
                [ortanca_kare[x::9] for x in range(0, 9)] +
                [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
                 for cs in ('123', '456', '789')
                 if not (rs in 'ABCGHI' and cs in '123789')])

tum_kareler = set(sol_ust_kare + sag_ust_kare + sol_alt_kare + sag_alt_kare + ortanca_kare)
tum_listeler = unitlist_a + unitlist_b + unitlist_c + unitlist_d + ortanca_liste

units = dict((s, [u for u in tum_listeler if s in u])
             for s in tum_kareler)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in tum_kareler)



if __name__ == '__main__':

    basari_durum = 0

    prompt = 1
    while prompt:
        txt = input("Dosya yolunu giriniz: ")
        try:
            f = open(txt, 'r')
            prompt = 0
        except FileNotFoundError:
            print("Dosya yolu bulunamadı.")
    samurai_grid = f.read().split('\n')

    for i in range(2):
        if i == 0:
            besli_thread = datetime.now()
            ans = samurai.solve(samurai_grid, i)
            besli_thread = datetime.now() - besli_thread
        else:
            onlu_thread = datetime.now()
            ans = samurai.solve(samurai_grid, i)
            onlu_thread = datetime.now() - onlu_thread


        if ans:
            basari_durum += 1
            sol_ust.update(sol_ust_kare)
            sag_ust.update(sag_ust_kare)
            sol_alt.update(sol_alt_kare)
            sag_alt.update(sag_alt_kare)
            orta.update(ortanca_kare)
            samurai.display_samurai(ans)



        veritabanina_yaz('sol_ust.csv', sol_ust)
        veritabanina_yaz('sag_ust.csv', sag_ust)
        veritabanina_yaz('sol_alt.csv', sol_alt)
        veritabanina_yaz('sag_alt.csv', sag_alt)
        veritabanina_yaz('ortanca.csv', orta)

    besli_grafik = []
    onlu_grafik = []


    besli_uzunluk = len(samurai.besli_thread_karesi)
    onlu_uzunluk = len(samurai.onlu_thread_karesi)

    try:
        besli = besli_thread.microseconds / besli_uzunluk
        onlu = onlu_thread.microseconds / onlu_uzunluk

        print('#' * 75)
        print("5'li Thread Zamanı:  ", besli_thread)
        print("10'lu Thread Zamanı: ", onlu_thread)
        print('#' * 75)


    except (ZeroDivisionError, TypeError):
        print("\nGeçersiz Sudoku!!!")

    for i in range(len(samurai.onlu_thread_karesi)):
        besli_grafik.append(round(besli + i * besli, 2))
        onlu_grafik.append(round(onlu + i * onlu, 2))

    if basari_durum >= 1:
        print("Samurai Sudoku Basariyla Cozuldu!..")
    else:
        print("Bu Samurai Sudokunun Cozumu Yok!!!")
        besli_thread = 0
        onlu_thread = 0

    plt.plot(besli_grafik, samurai.besli_thread_karesi, label="5'li THREAD")
    plt.plot(onlu_grafik, samurai.onlu_thread_karesi, label="10'lu THREAD")
    plt.xlabel('ZAMAN')
    plt.ylabel('KARE SAYISI')
    plt.title('5 THREAD - 10 THREAD')
    plt.legend()
    plt.show()