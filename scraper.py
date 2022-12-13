# import des package
import requests
import csv
import re
import math
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
    books = soup.find_all(class_="image_container")
#! DEBUT BOUCLE FOR IN LISTE LIVRE
    for index in range(len(books)):
        book_links.append("http://books.toscrape.com/catalogue/" +
                          books[index].a['href'].replace('../', ''))
#! DEBUT BOUCLE FOR IN LISTE LIVRE

#! DEBUT DE MA CONDITION
    next = soup.select_one("li.next>a")
    if (next != None):
        number_pages = int(
            soup.find(class_="form-horizontal").find("strong").string) / 20
        number_pages = math.ceil(number_pages)
    # !DEBUT DE MA FOR POUR CHANGER DE PAGE
        for page in range(2, number_pages + 1):
            link_finaly = re.findall("index.html|page...html$", url_category)
            page_x = f"page-{page}.html"
            soup = get_request_url(url_category.replace(
                str(link_finaly[0]), page_x))
            #! DEBUT BOUCLE FOR IN LISTE LIVRE
            books = soup.find_all(class_="image_container")
            for index in range(len(books)):
                book_links.append("http://books.toscrape.com/catalogue/" +
                                  books[index].a['href'].replace('../', ''))
            #!! FIN DE LA BOUCLE FOR IN LISTE DE LIVRE
#! FIN DE MA CONDITION
    return book_links


def get_informations_from_page(url_book):
    informations = []
    soup = get_request_url(url_book)
    all_td = soup.find_all('td')
    for td in all_td:
        informations.append(td.text)
    title = soup.find('h1').text
    informations[1] = title
    description = soup.select(".product_page > p")[0].text
    informations.insert(6, description)
    categorie = soup.select('.breadcrumb > li')[2].text
    informations.insert(7, categorie)
    image_selector = soup.select(".item > img")
    image_url = "http://books.toscrape.com/"+image_selector[0]['src']
    informations.append(image_url)
    informations.insert(0, url)
    informations.pop(5)

    return informations


def create_file(url_book):
    # Je fais appel a ma fonction pour recupere mes informations de la page
    details_of_my_book = get_informations_from_page(url_book)
    en_tete = ("Product_page_url", "upc", "Title", "Price_including_tax", "Price_excluding_tax",
               "Pumber_available", "Product_description", "Category", "Review_rating", "Image_url")

    with open('data.csv', 'a', newline="", encoding="utf-8") as fichier_csv:
        file_writer = csv.writer(fichier_csv)
        file_writer.writerow(en_tete)
        file_writer.writerow(details_of_my_book)


def main(url):
    #! JE RECUPERE TOUTES LES CATEGORIES
    all_categorys = get_all_categorys_link(url)
#! START BOUCLE
    for link in all_categorys:
        all_books = get_books_link(link)
        for book in all_books:
            create_file(book)
#! END BOUCLE
    # # principal_function(url)
    # # A FAIRE
    # # 1 - REGLER LES LIENS DANS LA FONCTION GET CATEGORY LINK
