pySudokuu
========

Solveur/générateur de Sudoku simple créé en Python.

Sur
-----

Solveur : Le programme scanne d'abord chaque grilles et s'il n'existe qu'une seule possibilité, alors il insère ce numéro. Le programme fait cela jusqu'à ce que la grille soit bloqué. Ensuite, il exécute une recherche DFS en arrière pour "essayer" les possibilités, en éliminant celles (et ses enfants) qui ne fonctionnent pas.

Nous avons visés la lisibilité et la simplicité du code au fil du temps, bien que ce programme puisse résoudre une grille de Sudoku en ~ 0,2 s en moyenne (notez que la résolution des grilles Sudoku est NP-complet).

Générateur : Le générateur commence avec une grille 9x9 vide et la remplit en itérant de la grilles en haut à gauche vers la grilles en bas à droite, et en remplissant les grilles en essayant des nombres aléatoires. Il vérifie si le nombre inséré fonctionne, et si c'est le cas, continue de manière récursive. Ensuite, la grille complète de 9x9 est réduite pour devenir le début d'une grille de Sudoku. Il génère une liste d'entiers 0-80 représentant les indices de la grille, puis brouille l'ordre. Pour réduire, nous essayons de supprimer le numéro au premier index de la liste, puis essayons de résoudre la grille. S'il existe plusieurs solutions, alors ce n'est pas une grille de Sudoku valide, alors à ce moment là, la dernière modification est annulée. Si des grilles faciles sont souhaitées, l'algorithme s'arrête après avoir trouvé une grille avec une solution unique. Si des grilles difficiles sont recherchés, alors même après avoir trouvé une grille valide, tous les indices restants sont essayés pour voir si la grille peut être rendu plus difficile. Les grilles difficiles ne sont pas seulement des tableaux uniques, mais des tableaux où vous ne pouvez plus supprimer de numéros sans détruire l'unicité de la solution.

Comment éxécuter: 
PS: Pour Julien on sait jamais...
----------
Pour exécuter le solveur :

    python pySudoku.py Sudokus.txt

Pour exécuter le générateur :

    python Generator.py

Bien sûr, vous pouvez utiliser le solveur avec n'importe quel fichier texte contenant des grilles Sudoku.
Le générateur écrit dans un fichier nommé "Sudokugrilles.txt", chaque grilles étant représenté par une ligne d'entiers lus du haut à gauche vers le bas à droite de la grille.