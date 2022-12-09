# import du package requests, celui ci me permet de faire des requetes HTTP
import requests
import csv
#  import de Bautifulsoup de bs4 pour recuperer les donner des fichier html ou XML
from bs4 import BeautifulSoup
from math import *

# ici je recupere l'URL principal du site
url = "http://books.toscrape.com/index.html"


def get_request_url(url):
    response = requests.get(url)
    if response.ok:  # si le resultat est ok je retourne le contenue
        return response.text


def get_all_link(url):
    # cette fonction permet de recupere tous les lien des categorie et des livres
    book_link = []
    category_link = []
    all_link = []
    # J'initialise les list qui vons recevoir les liens

    soup = BeautifulSoup(get_request_url(
        url), 'html.parser')
    # Je fait ma soupe

    category = (soup.select(".nav-list > li > ul > li > a"))
    book = soup.find_all(class_="image_container")
    book_per_page = soup.find_all("strong")[2].text
    # Je recupere les liens de mes categorie, de mon book, et le nombre de livre par page

    for i in range(0, 50):
        category_link.append("http://books.toscrape.com/" +
                             category[i]['href'].replace('../', ''))
    del category_link[16]
    # je boucle pour recuperer les liens et je supprime un index car il ne correspond a rien

    for i in range(int(book_per_page)):
        book_link.append("http://books.toscrape.com/" + book[i].a['href'])

    all_link = [category_link, book_link]
    return all_link
    # Je retourne toutes les listes dans une liste comunes
# ici je calcule le nombre de page et je change les page pour boucler mon resultat


def change_page(url):
    soup = BeautifulSoup(get_request_url(url), 'html.parser')
    # ici je prend le nombre de produit par categorie
    result = soup.find_all("strong")[1].text
    nbr_page_float = int(result) / 20
    if (nbr_page_float < 1):
        return nbr_page_float
    elif (nbr_page_float > 1):
        nbr_page = ceil(nbr_page_float)
        for page in range(1, nbr_page + 1):
            page_x = "page-" + str(page)+".html"
            url_change = "http://books.toscrape.com/catalogue/category/books/add-a-comment_18/" + page_x
            soup = BeautifulSoup(get_request_url(url_change))
# Recuperer les lien par livres


# recupere les information de la page
def get_informations_from_page(url):
    # Recuperation des informations de la page pour cree le CSV
    informations = []

    soup = BeautifulSoup(get_request_url(url), 'html.parser')
    # recupere les informations dans les <td> c'est à dire

    all_td = soup.find_all('td')
    for td in all_td:
        informations.append(td.text)

    # recuperation du titre
    title = soup.find('h1').text
    informations[1] = title
    # Recupération du commentaire
    description = soup.select(".product_page > p")[0].text
    informations.insert(6, description)
    categorie = soup.select('.breadcrumb > li')[2].text
    informations.insert(7, categorie)
    image_selector = soup.select(".item > img")
    image_url = "http://books.toscrape.com/" + image_selector[0]['src']
    informations.append(image_url)
    informations.insert(0, url)
    informations.pop(5)

    return informations


# cette fonction me permet de cree un fichier csv
def create_file(url):
    # Je fais appel a ma fonction pour recupere mes informations de la page
    details_of_my_book = get_informations_from_page(url)
    en_tete = ("Product_page_url", "upc", "Title", "Price_including_tax", "Price_excluding_tax",
               "Pumber_available", "Product_description", "Category", "Review_rating", "Image_url")

    with open('data.csv', 'w') as fichier_csv:
        file_writer = csv.writer(fichier_csv)
        file_writer.writerow(en_tete)
        file_writer.writerow(details_of_my_book)
