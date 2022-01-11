"""
Nom: pySudoku.py

Essayez d'abord de résoudre en remplissant les cellules avec une seule possibilité.
Si cela ne peut pas aller plus loin, utilisez un DFS de retour en arrière (recherche en profondeur d'abord)
pour essayer les solutions possibles. 
Dès qu'une solution est trouvée, il termine l'algorithme et l'imprime.

L'algorithme suppose que les cellules vides sont signalées par un 0.
"""

import fileinput
import time

def print_sudoku(s):
    """
    Formate la grille de Sudoku actuellement dans une liste 2D en
    une grille avec des lignes séparant les blocs pour plus de lisibilité
    """
    for row in range(9):
        for col in range(9):
            print(s[row][col], end=' ')
            if col+1 == 3 or col+1 == 6:
                print(" | ", end=' ')
        if row+1 == 3 or row+1 == 6:
            print("\n" + "-"*25, end=' ')
        print()
    print()

def test_cell(s, row, col):
    """
    Étant donné le nombre de s, de ligne et de colonne d'une grille de Sudoku, renvoyez une liste qui représente
    les nombres valides qui peuvent aller dans cette cellule. 0 = possible, 1 = impossible
    """
    used = [0]*10
    used[0] = 1
    block_row = row // 3
    block_col = col // 3

    # Row and Column
    for m in range(9):
        used[s[m][col]] = 1;
        used[s[row][m]] = 1;

    # Square
    for m in range(3):
        for n in range(3):
            used[s[m + block_row*3][n + block_col*3]] = 1

    return used

def initial_try(s):
    """
    Essayez de résoudre la grille en itérant à travers chaque
    cellule et déterminer les nombres possibles dans cette cellule. Si un seul numero possible
    existe, remplissez-le et continuez jusqu'à ce que la grille soit bloqué.
    """
    stuck = False

    while not stuck:
        stuck = True
        # Itérer à travers la grille Sudoku
        for row in range(9):
            for col in range(9):
                used = test_cell(s, row, col)
                # Plus d'une possibilité
                if used.count(0) != 1:
                    continue

                for m in range(1, 10):
                    # Si la cellule actuelle est vide et qu'il n'y a qu'une seule possibilité.
                    # puis remplissez la cellule actuelle
                    if s[row][col] == 0 and used[m] == 0:
                        s[row][col] = m
                        stuck = False
                        break

def DFS_solve(s, row, col):
    """
    Résolvez la grille en effectuant récursivement DFS
    qui expérimente les solutions possibles et en utilisant le backtracking (en éliminant les
    essais invalides et tous les cas possibles découlant de ces essais)
    """
    if row == 8 and col == 8:
        used = test_cell(s, row, col)
        if 0 in used:
            s[row][col] = used.index(0)
        return True

    if col == 9:
        row = row+1
        col = 0

    if s[row][col] == 0:
        used = test_cell(s, row, col)
        for i in range(1, 10):
            if used[i] == 0:
                s[row][col] = i
                if DFS_solve(s, row, col+1):
                    return True

        #Ensuite, nous avons essayé 1-9 sans succès
        s[row][col] = 0
        return False

    return DFS_solve(s, row, col+1)

def main():
    start = time.time()
    num_grilles = 0
    s = []
    text = ""

    for line in fileinput.input():
        line = ' '.join(line.split())
        text += line

    while len(text) > 0:
        l = []

        # Obtenez une rangée de nombres.
        while len(l) < 9:
            if text[0].isdigit():
                l.append(int(text[0]))
            text = text[1:]

        # Insérez cette ligne dans la grille du Sudoku.
        s.append(l)

        if len(s) == 9:
            num_grilles += 1
            print("Nombres Grilles{:d}".format(num_grilles))
            print("Original:")
            print_sudoku(s)

            initial_try(s)
            for line in s:
                if 0 in line:
                    DFS_solve(s, 0, 0)
                    break

            print("Solution:")
            print_sudoku(s)

            print("="*30)
            s = []

    print("{:.2f} secondes pour résoudre {} la grilles".format(time.time() - start, num_grilles))

if __name__ == "__main__":
    main()
