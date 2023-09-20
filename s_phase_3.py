import requests
from bs4 import BeautifulSoup
from s_phase_2 import etl_cat
from s_phase_1 import etl, charger_donnees



def cat_booktoScrape():
    # lien de la page à scrapper
    url = "http://books.toscrape.com/"
    reponse = requests.get(url)
    page = reponse.content

    # transforme (parse) le HTML en objet BeautifulSoup
    soup = BeautifulSoup(page, "html.parser")

    # récupération de toutes les categories
    categories = soup.find("ul", class_="nav nav-list").find("ul").findAll("li")

    tab_category = []
    tab_nom = []
    for cat in categories:
        category = "http://books.toscrape.com/"+cat.find("a").get("href")
        nom = cat.text.strip()
        tab_nom.append(nom)
        tab_category.append(category)
    return tab_category, tab_nom

#initialise quelques variables et appels des fonctions
i = 0
bookstoscrape = cat_booktoScrape()
for category, nom in zip(bookstoscrape[0],bookstoscrape[1]):
    i = i+1
    print(str(i))
    books = etl_cat(category)
    titles = []
    categories = []
    urls = []
    upcs = []
    price_including_taxes = []
    price_excluding_taxes = []
    number_availables = []
    review_ratings = []
    product_descriptions = []
    images = []

    en_tete = ["title", "Category", "url", "upc", "price_including_taxe", "price_excluding_taxe", "number_available", "review_rating", "product_description", "image"]

    for book in books:
        result = etl(book)

        titles = titles + result[0]
        categories = categories + result[1]
        urls = urls + result[2]
        upcs = upcs + result[3]
        price_including_taxes = price_including_taxes + result[4]
        price_excluding_taxes = price_excluding_taxes + result[5]
        number_availables = number_availables + result[6]
        review_ratings = review_ratings + result[7]
        product_descriptions = product_descriptions + result[8]
        images = images + result[9]

        charger_donnees(f"{nom}.csv", en_tete, titles, categories, urls, upcs , price_including_taxes, price_excluding_taxes, number_availables, review_ratings, product_descriptions, images)