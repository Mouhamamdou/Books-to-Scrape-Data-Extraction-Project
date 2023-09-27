import requests
from bs4 import BeautifulSoup
from s_phase_2 import livres_par_cat
from s_phase_1 import etl, charger_donnees


def tous_les_categories():
    """ Cette fonction extrait toutes les catégories se trouvant dans le site BooktoScrape """
    url = "http://books.toscrape.com/"
    reponse = requests.get(url)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # récupération de toutes les categories dans un dictionnaire, la valeur est l'url de catégorie
    categories = soup.find("ul", class_="nav nav-list").find("ul").findAll("li")
    categories_dict = {cat.text.strip(): "http://books.toscrape.com/" + cat.find("a").get("href") for cat in categories}

    return categories_dict


if __name__ == "__main__":

    # retounre toutes les catégories (nom et url) se trouvant dans BooktoScrape, sous forme de dictionnaire
    les_categories = tous_les_categories()

    i = 0
    for nom_categorie, url_categorie in les_categories.items():
        i += 1
        print(f"{i} eme categorie ==> {nom_categorie}: {url_categorie}")

        # retourne tous les livres (titre et url) contenus dans une catégorie
        books_in_cat = livres_par_cat(url_categorie)
        all_books = {}
        for titre, url_book in books_in_cat.items():

            # retourne un dictionnaire contenant les données de chaque livre
            data_book = etl(url_book)

            # fusionner les données des livres en dictionnaire de listes de données
            for key in set(all_books.keys()) | set(data_book.keys()):
                all_books[key] = all_books.get(key, []) + data_book.get(key, [])

        # ecrire les données dans un fichier csv
        charger_donnees(f"{nom_categorie}.csv", all_books)