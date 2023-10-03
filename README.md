# Projet-2

Le projet comprend 3 script python : s_phase_1.py, s_phase_2.py et s_phase_3.py.

On y a également inclut un fichier requirements.txt qui contient toutes les librairies nécessaires à l'éxecution du projet.

Commencez par créer un environnement virtuel avec la commande suivante :
python -m vene < nom_de_l'environnement >

Ensuite déplacez vous dans le dossier Scripts de l'environnement virtuel,
et activer celui-ci grâce à la commande source activate

L'execution du code se fait selon le besoin :

S'il est exécuté à partir du script s_phase_3.py, le programme va récupérer toutes les catégories existantes dans le site BooktoScrape,
et extraire les données des livres de chaque catégorie.
Le résultat est un ensemble de fichier csv pour chaque catégorie, contenant les données extraites des livres de la catégorie.
Le programme crée également des sous dossiers d'image pour catégorie contenant les images téléchargées pour chaque livre.

Le programme peut également être exécuté à partir du script s_phase_2.py.
Dans ce cas il faut renseigner l'url d'une catégorie de livre.
Le résultat est un fichier csv de la catégorie renseignée en entrée, contenant les données de tous les livres de cette catégorie.

Enfin si le programme est lancé dans le script s_phase_1.py, on doit renseigner l'ur d'un livre en entrée.
Il va générer un fichier csv contenant les données de ce livre.
