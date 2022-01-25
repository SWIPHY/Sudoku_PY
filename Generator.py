import pySudoku
import random
import time

def toString(sudoku):
    """
    Formate une liste 2D du sudoku en une ligne d'entiers
    pour une écriture facile.
    """
    sortie = ""
    for i in range(9):
        for j in range(9):
            sortie += str(sudoku[i][j])
    return sortie + "\n"

def vérif_Validité(sudoku, row, colonne):
    """
    Renvoie True si une cellule donnée est valide dans le Sudoku, sinon Faux. 
    Une case est valide si le nombre dans cette meme case n'est pas présente dans l'une des autres cases de la même ligne,
    de la même colonne ou du même bloc.
    """
    block_row = row // 3
    block_colonne = colonne // 3

    for m in range(9):
        if sudoku[row][m] != 0 and m != colonne and sudoku[row][m] == sudoku[row][colonne]:
            return False
        if sudoku[m][colonne] != 0 and m != row and sudoku[m][colonne] == sudoku[row][colonne]:
            return False

    # Block
    for m in range(3):
        for n in range(3):
            newRow = m + block_row*3
            newCol = n + block_colonne*3
            if sudoku[newRow][newCol] != 0 and newRow != row and newCol != colonne\
            and sudoku[newRow][newCol ] == sudoku[row][colonne]:
                return False

    return True

def populateBoard(sudoku, row, colonne):
    """
    À partir d'une grille 9x9 de 0, cette fonction remplit récursivement
    la grille. Il fait une liste d'entiers de 1 à 9, mélange l'ordre et
    essaie le premier nombre de la liste dans la case actuelle. Si le nombre inséré
    fonctionne, il passe  la suivantee. Si l'entier ne fonctionne pas alors
    il essaie le suivant dans la liste. Si aucun des nombres entiers ne fonctionne, alors
    il défini sur vide et retourne false.
    """
    if row == 8 and colonne == 8:
        used = pySudoku.test_cell(sudoku, row, colonne)
        sudoku[row][colonne] = used.index(0)
        return True

    if colonne == 9:
        row = row+1
        colonne = 0

    temp = list(range(1, 10))
    random.shuffle(temp)
    
    for i in range(9):
        sudoku[row][colonne] = temp[i]
        if vérif_Validité(sudoku, row, colonne):
            if populateBoard(sudoku, row, colonne+1):
                return True
    sudoku[row][colonne] = 0
    return False

def DFS_solve(copy_s, row, colonne):
    """
    Résout récursivement la grille avec un retour en arrière un utilisant
    l'algorithme DFS, en retournant le nombre de solutions trouvées.
    Commence à la ligne 0 et à la colonne 0, et continue vers la droite et
    en bas des rangées.
    """
    num_solutions = 0

    # Atteint les dernières cellules sans aucune erreur, il y a donc une solution
    if row == 8 and colonne == 8:
        return num_solutions + 1

    if colonne == 9:
        row = row+1
        colonne = 0

    if copy_s[row][colonne] == 0:
        # Used = liste de taille 10 représentant quels nombres sont possibles
        # Dans la grille: 0 = possible, 1 = impossible.
        used = pySudoku.test_cell(copy_s, row, colonne)
        # Aucune solution possible. Renvoie 0 pour le nombre de solutions.
        if 0 not in used:
            return 0

        while 0 in used:
            copy_s[row][colonne] = used.index(0)
            used[used.index(0)] = 1
            num_solutions += DFS_solve(copy_s, row, colonne+1)

        # Reached here? Then we tried 1-9 without success
        copy_s[row][colonne] = 0
        return num_solutions

    num_solutions += DFS_solve(copy_s, row, colonne+1)
    return num_solutions

def reduce_sudoku(sudoku, niveau_difficultée):
    """
    Génére d'abord une liste d'entiers 0-80 représentant les indices
    dans la grille. S'il existe plus d'une solution, alors ce n'est pas une
    une grille de Sudoku valide, ce qui annule alors la dernière modification. 
    Si des grilles faciles sont choisis, une solution unique est trouvé, et donc l'algorithme s'arrête. 
    Si des grilles difficiles sont choisis, même après avoir trouvé un grille valide, tous les autres indices doivent être testés pour voir si la grille peut être rendu plus difficile.
    """
    indices = list(range(81))
    random.shuffle(indices)

    while indices:
        row = indices[0] // 9
        colonne = indices[0] % 9
        temp = sudoku[row][colonne]
        sudoku[row][colonne] = 0
        indices = indices[1:]

        copy_s = [l[:] for l in sudoku]

        pySudoku.initial_try(copy_s)

        for line in copy_s:
            if 0 in line:
                num_solutions = DFS_solve(copy_s, 0, 0)
               # Si la grille n'a pas de solution unique, alors ça annule la dernière insertion.
                if num_solutions > 1:
                    sudoku[row][colonne] = temp
                    if niveau_difficultée == "E" or niveau_difficultée == "e":
                        return
                break

    return
"""
Ouvre le fichier txt SudokuGrilles et utilise la fonction write 'w'.
Ensuite pose la question de 'Combien de grille de Sudoku voulez-vous générer ?'.
Puis demande 'Grilles facile ou difficile (e ou d)'.
Enfin le programme génère la grille ou les grilles du Sudoku dans le fichier qui vient de se créér.
"""

def main():
    f = open("SudokuGrilles.txt", "w")
    entrée_user = int(input("Combiens de grilles souhaitez-vous générer ? : "))
    niveau_difficultée = input("Niveau Easy ou Difficile ? (e ou d) : ")
    start = time.time()

    for _ in range(entrée_user):
        # 9 x 9
        sudoku = [[0]*9 for _ in range(9)]

        populateBoard(sudoku, 0, 0)
        reduce_sudoku(sudoku, niveau_difficultée)
        sortie = toString(sudoku)
        f.write(sortie)

    print("{:.2f} seconds pour créer {} grilles de Sudoku.".format(time.time() - start, entrée_user))

if __name__ == '__main__':
    main()
