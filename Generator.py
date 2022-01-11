import pySudoku
import random
import time

def toString(s):
    """
    Formate une liste 2D du sudoku en une ligne d'entiers
    pour une écriture facile.
    """
    output = ""
    for i in range(9):
        for j in range(9):
            output += str(s[i][j])
    return output + "\n"

def checkValid(s, row, col):
    """
    Renvoie True si une cellule donnée est valide dans le Sudoku, sinon Faux. 
    Une case est valide si le nombre dans cette meme case n'est pas présente dans l'une des autres cases de la même ligne,
    de la même colonne ou du même bloc.
    """

    """
    row = ligne
    column = colonnes
    """

    block_row = row // 3
    block_col = col // 3

    # Lignes et Colonnes
    # Ignorer les espaces vides
    for m in range(9):
        if s[row][m] != 0 and m != col and s[row][m] == s[row][col]:
            return False
        if s[m][col] != 0 and m != row and s[m][col] == s[row][col]:
            return False

    # Block
    for m in range(3):
        for n in range(3):
            newRow = m + block_row*3
            newCol = n + block_col*3
            if s[newRow][newCol] != 0 and newRow != row and newCol != col\
            and s[newRow][newCol ] == s[row][col]:
                return False

    return True

def populateBoard(s, row, col):
    """
    À partir d'une grille 9x9 de 0, cette fonction remplit récursivement
    la grille. Il fait une liste d'entiers de 1 à 9, mélange l'ordre et
    essaie le premier nombre de la liste dans la case actuelle. Si le nombre inséré
    fonctionne, il passe  la suivantee. Si l'entier ne fonctionne pas alors
    il essaie le suivant dans la liste. Si aucun des nombres entiers ne fonctionne, alors
    il défini sur vide et retourne false.
    """
    if row == 8 and col == 8:
        used = pySudoku.test_cell(s, row, col)
        s[row][col] = used.index(0)
        return True

    if col == 9:
        row = row+1
        col = 0

    temp = list(range(1, 10))
    random.shuffle(temp)
    # Fill Sudoku
    for i in range(9):
        s[row][col] = temp[i]
        if checkValid(s, row, col):
            if populateBoard(s, row, col+1):
                return True
    s[row][col] = 0
    return False

def DFS_solve(copy_s, row, col):
    """
    DFS : L'algorithme de parcours en profondeur (ou DFS, pour Depth-First Search) est un algorithme de parcours d'arbre, 
    et plus généralement de parcours de graphe. 
    Il se décrit naturellement de manière récursive. 
    Son application la plus simple consiste à déterminer s'il existe un chemin d'un sommet à un autre.
    """
    
    """
    Résout récursivement la grille avec un retour en arrière un utilisant
    l'algorithme DFS, en retournant le nombre de solutions trouvées.
    Commence à la ligne 0 et à la colonne 0, et continue vers la droite et
    en bas des rangées.
    """
    num_solutions = 0

    # Atteint les dernières cellules sans aucune erreur, il y a donc une solution
    if row == 8 and col == 8:
        return num_solutions + 1

    if col == 9:
        row = row+1
        col = 0

    if copy_s[row][col] == 0:
        # Used = liste de taille 10 représentant quels nombres sont possibles
        # Dans la grille: 0 = possible, 1 = impossible.
        used = pySudoku.test_cell(copy_s, row, col)
        # Aucune solution possible. Renvoie 0 pour le nombre de solutions.
        if 0 not in used:
            return 0

        while 0 in used:
            copy_s[row][col] = used.index(0)
            used[used.index(0)] = 1
            num_solutions += DFS_solve(copy_s, row, col+1)

        copy_s[row][col] = 0
        return num_solutions

    num_solutions += DFS_solve(copy_s, row, col+1)
    return num_solutions

def reduce_sudoku(s, difficulty):
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
        col = indices[0] % 9
        temp = s[row][col]
        s[row][col] = 0
        indices = indices[1:]

        copy_s = [l[:] for l in s]

        pySudoku.initial_try(copy_s)

        for line in copy_s:
            if 0 in line:
                num_solutions = DFS_solve(copy_s, 0, 0)
                # Si la grille n'a pas de solution unique, alors ça annule la dernière insertion.
                if num_solutions > 1:
                    s[row][col] = temp
                    # Si nous voulons des grilles faciles, nous nous arrêterions ici après avoir trouvé
                    # le premier puzzle avec une solution unique sans essayer de se compliquer la taache en essayant de supprimer d'autres éléments et en voyant
                    # s'il existe une autre grille plus difficile avec une solution unique...
                    """
                    E et e = easy => facile
                    """
                    if difficulty == "E" or difficulty == "e":
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
    user_input = int(input("Combien de grille de Sudoku voulez-vous générer ? : "))
    difficulty = input("Grilles facile ou difficile (e ou d) : ")
    start = time.time()

    for _ in range(user_input):
        # 9 x 9 grid of 0s
        s = [[0]*9 for _ in range(9)]

        populateBoard(s, 0, 0)
        reduce_sudoku(s, difficulty)
        output = toString(s)
        f.write(output)

    print("{:.2f} secondes pour trouver {} Sudoku Grilles.".format(time.time() - start, user_input))

if __name__ == '__main__':
    main()
