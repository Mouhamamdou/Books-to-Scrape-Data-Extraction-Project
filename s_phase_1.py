import requests
from bs4 import BeautifulSoup
import csv
import os
import urllib.request

# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(elements):
    resultat = []
    for element in elements:
        resultat.append(element.text)
    return resultat

# charger la donnée dans un fichier csv
def charger_donnees(nom_fichier, en_tete, titles, categories, urls, upcs, price_in_taxes, price_exc_taxes, number_availables, review_ratings, product_descriptions, inages):
    with open(nom_fichier, 'w', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        # zip permet d'itérer sur deux listes à la fois
        for title, categorie, url, upc, price_in_taxe, price_exc_taxe, number_available, review_rating, product_description, inage in zip(titles, categories, urls, upcs, price_in_taxes, price_exc_taxes, number_availables, review_ratings, product_descriptions, inages):
            writer.writerow([title, categorie, url, upc, price_in_taxe, price_exc_taxe, number_available, review_rating, product_description, inage])
def etl(url):
    # lien de la page à scrapper
    reponse = requests.get(url)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # récupération de toutes les informations produits
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
    image_url = []
    image_url.append(img)

    category = extraire_donnees(soup.find_all("a")[3])

    url_tab = []
    url_tab.append(url)

    try:
        os.makedirs("image")
    except FileExistsError:
        print("directory image already exists")

    try:
        os.makedirs("image/"+category[0])
    except FileExistsError:
        print(f"directory {category[0]} already exists")

    try:
        urllib.request.urlretrieve(img, f"image/{category[0]}/{title[0]}.png")
    except OSError:
        print(f"{title} ,image not found")

    return title, category, url_tab, upc, price_inc_taxe, price_exc_taxe, number_available, review_rating, description, image_url

