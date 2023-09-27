import requests
from bs4 import BeautifulSoup
import csv
import os
import urllib.request


def extraire_donnees(elements):
    """ Cette fonction retourne chaque type de données de livre dans une liste de string """
    resultat = [element.text for element in elements]
    return resultat


def charger_donnees(nom_fichier, data):
    """ Cette fonction écrit dans un fichier csv les données extraites pour un livre """

    with open(nom_fichier, 'w', encoding='utf-8', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')

        # Ecrire les entetes
        writer.writerow(data.keys())

        # Etant donnees que toutes les listes ont la même longueur
        num_rows = len(next(iter(data.values()), []))

        # Ecrire les données
        for i in range(num_rows):
            writer.writerow([data[key][i] if i < len(data[key]) else '' for key in data.keys()])


def etl(url):
    """ Cette fonction extrait, transforme et charge les données pour un livre """

    reponse = requests.get(url)
    page = reponse.content
    soup = BeautifulSoup(page, "html.parser")

    product_info = soup.find("table", class_="table table-striped").find_all('td')

    upc = extraire_donnees(product_info[0])
    price_exc_taxe = extraire_donnees(product_info[2])
    price_inc_taxe = extraire_donnees(product_info[3])
    number_available = extraire_donnees(product_info[5])
    review_rating = extraire_donnees(product_info[6])
    try:
        description = extraire_donnees(soup.find('p', attrs={'class': None}))
    except TypeError:
        description = ["pas de description"]

    title = extraire_donnees(soup.find("h1"))

    web_url = "http://books.toscrape.com/"
    img = soup.find("img").get("src").replace("../../", web_url)
    image_url = [img]

    category = extraire_donnees(soup.find_all("a")[3])

    url_tab = [url]

    try:
        os.makedirs("image")
    except FileExistsError:
        print("directory image already exists")

    try:
        os.makedirs("image/" + category[0])
    except FileExistsError:
        print(f"directory {category[0]} already exists")

    try:
        urllib.request.urlretrieve(img, f"image/{category[0]}/{title[0]}.png")
    except OSError:
        print(f"{title} ,image not found")

    # Retourne les données sous un dictionnaire
    data = {
        "title": title,
        "category": category,
        "url": url_tab,
        "upc": upc,
        "price_inc_taxe": price_inc_taxe,
        "price_exc_taxe": price_exc_taxe,
        "number_available": number_available,
        "review_rating": review_rating,
        "description": description,
        "image_url": image_url
    }

    return data


if __name__ == "__main__":
    url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

    # retourne les données d'un livre sous forme de dictionnaire
    result = etl(url)

    # écrire les données dans un fichier csv
    charger_donnees("un_livre.csv", result)