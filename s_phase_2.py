import requests
from bs4 import BeautifulSoup
from s_phase_1 import etl, charger_donnees


def extraire_url_books(elements):
    """ Cette fonction récupère les url des livres dans un dictionnaire, le titre represente la clé """
    resultat = {}
    for element in elements:
        titre = element.find('a').get('title')
        url = element.find('a').get('href').replace("../../../", "http://books.toscrape.com/catalogue/")
        resultat[titre] = url
    return resultat

def livres_par_cat(url_category):
    """ Cette fonction extarit les urls et titres de tous les livres d'une catégorie donnée """
    tous_livres = {}

    # lien de la page à scrapper
    reponse = requests.get(url_category)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # si la categorie contient plusieurs pages
    try:
        next = soup.find("li", class_="next").text
    except AttributeError:
        next = ""

    # récupération de tous les titres et URLs de chaque livre
    if next == "next":
        page = soup.find("li", class_="current").text.strip()[10]

        for i in range(int(page)):
            url_category_next = url_category.replace("index.html", f"page-{i+1}.html")

            reponse_next = requests.get(url_category_next)
            page_next = reponse_next.content
            soup_next = BeautifulSoup(page_next, "html.parser")

            # recupérer titres et url de livre de niveau 3
            livres = extraire_url_books(soup_next.find_all("h3"))

            # Mise à jour du dictionnaire avec les titres et les URL obtenus
            tous_livres.update(livres)
    else:
        livres = extraire_url_books(soup.find_all("h3"))

        # Mise à jour du dictionnaire avec les titres et les URL obtenus
        tous_livres.update(livres)

    return tous_livres


if __name__ == "__main__":

    url_cat = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"

    # retourne un dictionnaire contenant les titres et les url des livres de la catégorie choisie
    book_in_cat = livres_par_cat(url_cat)
    all_books = {}
    for title, url_book in book_in_cat.items():

        #retourner les données de chaque livre dans un dictionnaire
        data_book = etl(url_book)

        #fusionner les données de tous les livres d'une catégorie sous forme de dictionnaire de listes concaténées
        for key in set(all_books.keys()) | set(data_book.keys()):
            all_books[key] = all_books.get(key, []) + data_book.get(key, [])

    # retourne un fichier csv contenant les données de tous les livres d'une catégorie donnée
    charger_donnees("catégorie.csv",all_books)