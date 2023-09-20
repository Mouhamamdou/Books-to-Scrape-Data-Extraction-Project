import requests
from bs4 import BeautifulSoup
from s_phase_1 import etl, charger_donnees


# récupère les url des livres dans une liste

def extraire_url_books(elements):
    resultat = []
    for element in elements:
        resultat.append(element.find('a').get('href').replace("../../../","http://books.toscrape.com/catalogue/"))
    return resultat


def etl_cat(url_category):
    tous_livres = []
    # lien de la page à scrapper"
    reponse = requests.get(url_category)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # si la categorie contient plusieurs pages
    try:
        next = soup.find("li", class_="next").text
    except AttributeError:
        next = ""

    # récupération de tous les titres
    if next == "next":
        page = soup.find("li", class_="current").text.strip()[10]

        for i in range(int(page)):
            url_category_next = url_category.replace("index.html", f"page-{i+1}.html")

            reponse_next = requests.get(url_category_next)
            page_next = reponse_next.content
            soup_next = BeautifulSoup(page_next, "html.parser")
            url_book = extraire_url_books(soup_next.find_all("h3"))
            tous_livres = tous_livres + url_book
    else:
        url_book = extraire_url_books(soup.find_all("h3"))
        tous_livres = tous_livres + url_book


    return tous_livres