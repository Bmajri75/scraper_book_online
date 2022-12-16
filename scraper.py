# import des package
import requests
import csv
import re
import math
import os
from bs4 import BeautifulSoup


# je recupere l'URL  qui sera envoyé en requette
url = 'http://books.toscrape.com/index.html'


def get_request_url(url):
    # Ma fonction prend en entré une URL
    #! => renvoie ma variable Soup avec le contenue de la page parsé
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


def get_all_categorys_link(url):
    #  1 - Ma fonction prend en entrée un lien de la page principal,
    #  2 - Elle fait appel à la fonction get_request_url()
    #!  3 - => Elle renvoie une liste de tout les liens de la partie Category
    #! category_link[]
    soup = get_request_url(url)
    category_link = []
    category = (soup.select(".nav-list > li > ul > li > a"))
    for i in range(0, len(category)):
        category_link.append(
            "http://books.toscrape.com/"+category[i]["href"])
    return category_link


def get_books_link(url_category):
    #  1 - Ma fonction prend en entrée un lien de la page category,
    #  2 - Elle fait appel à la fonction get_request_url()
    #!  3 - => Elle renvoie une liste de tout les liens de la partie Livre
    #! book_link[]
    book_links = []
    soup = get_request_url(url_category)
    # Quoi qu'il en soit je boucle une premiere fois
    books = soup.find_all(class_="image_container")
    for index in range(len(books)):
        book_links.append("http://books.toscrape.com/catalogue/" +
                          books[index].a['href'].replace('../', ''))
    # Je recupere le next de la page si il y en a
    next = soup.select_one("li.next>a")
    if (next != None):
        # Je calcule le nombre de page que je divise par 20 et j'arrondie au nbr supperieur
        number_pages = int(
            soup.find(class_="form-horizontal").find("strong").string) / 20
        number_pages = math.ceil(number_pages)
        for page in range(2, number_pages + 1):
            link_finaly = re.findall("index.html|page...html$", url_category)
            page_x = f"page-{page}.html"
            soup = get_request_url(url_category.replace(
                str(link_finaly[0]), page_x))
            books = soup.find_all(class_="image_container")
            for index in range(len(books)):
                book_links.append("http://books.toscrape.com/catalogue/" +
                                  books[index].a['href'].replace('../', ''))
    return book_links


def get_informations_from_page(url_book):
    #  1 - Ma fonction prend en entrée un lien de la page du livre,
    #  2 - Elle fait appel à la fonction get_request_url()
    #!  3 - => Elle renvoie une liste de tout les informations demandé du Livre
    #! informatios[]
    informations = []
    soup = get_request_url(url_book)
    all_td = soup.find_all('td')
    for td in all_td:
        informations.append(td.text)
    title = soup.find('h1').text
    informations[1] = title
    description = soup.find("p", class_="")
    if description:
        informations.insert(6, description.text)
    else:
        informations.insert(6, "no description")
    categorie = soup.select('.breadcrumb > li')[2].text
    informations.insert(7, categorie)
    image_selector = soup.select(".item > img")
    image_url = "http://books.toscrape.com/"+image_selector[0]['src']
    informations.append(image_url)
    informations.insert(0, url_book)
    informations.pop(5)

    return informations


def main(url):
    #  1 - Ma fonction prend en entrée  url de la page d'accueil,
    #  2 - elle reprend toutes mes fonctions
    #!  3 - => Elle renvoie  les fichiers et dossier demandés
    #! Datas/ lescategories.csv
    #! images/photo.jpg
    all_categorys = get_all_categorys_link(url)
    # une premiere boucle pour recuperer les categories
    for link in all_categorys:
        details_of_my_book = []
        all_books = get_books_link(link)
        # chaque categories boucle sur chaque livre et recupere les liesn
        for book in all_books:
            info_book = get_informations_from_page(book)
        # Je fait une zone tempon dans le details of my books cette liste permet
        # d'utiliser la fonction writerows( pour avoir l'ecriture du fichier en une fois et juste un entete)
            details_of_my_book.append(info_book)
            category_name = re.sub("\s", "", info_book[7])
            book_name = re.sub("\s", "", info_book[2])

            # je recupere mes get_informations_from_pagesi ma requettes est ok
            img = requests.get(info_book[9])
            if img.ok:
                new_book_name = book_name.replace("/", "_")
                os.makedirs("./Images", exist_ok=True)
                with open(f"Images/{new_book_name}.jpg", 'wb') as file:
                    file.write(img.content)
                print(
                    f"L'image {info_book[9]} est bien telechargé dans le dossier ./Images")
        en_tete = ("Product_page_url", "upc", "Title", "Price_including_tax", "Price_excluding_tax",
                   "Pumber_available", "Product_description", "Category", "Review_rating", "Image_url")
        os.makedirs("./Datas", exist_ok=True)
        with open(f"./Datas/{category_name}.csv", 'w', newline="",  encoding="utf-8") as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(en_tete)
            writer.writerows(details_of_my_book)
            print(
                f"Les informations concernant {info_book[7]} sont bien telechargés dans le dossier ./Datas")


main(url)
