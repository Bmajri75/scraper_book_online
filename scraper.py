# import des package
import requests
import csv
import re
from bs4 import BeautifulSoup


# je recupere l'URL  qui sera envoyé en requette
url = "http://books.toscrape.com/index.html"


def get_request_url(url):
    # Ma fonction prend en entré une URL
    #! => renvoie ma variable Soup avec le contenue de la page parsé
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


def get_next_pages(url_category):
    soup = get_request_url(url_category)
    if (soup.find(class_="next")):
        next = soup.find(class_="next")
        nbr_page = re.findall("index.html|page...html$", url_category)
        page_x = next.a['href']
        next_page_url = url_category.replace(str(nbr_page[0]), page_x)
        return get_next_pages(next_page_url)
    return url_category


# ERREUR VIEN De ICI
'''
a l'appel de la recursivité de la fonction get_next_pages() celle ci renvoie none
cependent la variable next_page_url renvoie bien la str attendue 
'''

# print(get_next_pages(
#     'http://books.toscrape.com/catalogue/category/books/add-a-comment_18/index.html'))


def get_categorys_link(url):
    #  1 - Ma fonction prend en entrée un lien de la page principal,
    #  2 - Elle fait appel à la fonction get_request_url()
    #!  3 - => Elle renvoie une liste de tout les liens de la partie Category
    #! category_link[]
    soup = get_request_url(url)
    category_link = []
    category = (soup.select(".nav-list > li > ul > li > a"))

    for i in range(0, 50):
        category_link.append(
            "http://books.toscrape.com/" + category[i]['href'])
        soup = get_request_url(category_link[i])
        if (soup.find(class_="next")):
            print("PLUSIEURS PAGE ICI JE RAJOUTE" + category_link[i])
            category_link.append(get_next_pages(category_link[i]))
        else:
            print("RIEN ICI AU NEXT")
        #     category_link.append(get_next_pages(category_link[i]))
    return category_link


print(get_categorys_link(url))


def get_books_link(url_category):
    #  1 - Ma fonction prend en entrée un lien de la page category,
    #  2 - Elle fait appel à la fonction get_request_url()
    #!  3 - => Elle renvoie une liste de tout les liens de la partie Livre
    #! book_link[]
    soup = get_request_url(url_category)
    book_link = []
    books = soup.find_all(class_="image_container")
    for i in range(0, len(books)):
        book_link.append(
            "http://books.toscrape.com/catalogue/" + books[i].a['href'].replace('../', ''))
    return book_link


def get_informations_from_page(url_book):
    # Recuperation des informations de la page pour cree le CSV
    informations = []

# recupere les informations dans les <td> c'est à dire
    soup = get_request_url(url_book)

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


def create_file(url_book):
    # Je fais appel a ma fonction pour recupere mes informations de la page
    details_of_my_book = get_informations_from_page(url_book)
    en_tete = ("Product_page_url", "upc", "Title", "Price_including_tax", "Price_excluding_tax",
               "Pumber_available", "Product_description", "Category", "Review_rating", "Image_url")

    with open('data.csv', 'a') as fichier_csv:
        file_writer = csv.writer(fichier_csv)
        file_writer.writerow(en_tete)
        file_writer.writerow(details_of_my_book)


def main(url):
    """
    2 - je boucle les categories
        2-a je prend une categorie
            je lance une requetes pour la page cstegorie
                je lance une requetes pour le premier livre
                   je recupere les informations pour mon premier livre
                    je cree mon fichier CSV
                je lance une requettes pour mon second livre
                    (je recupere les informations que je rajoute au fichier csv deja cree )
                    (ou je cree un dictonnaire avec toutes les donnée et je cree le fichier une fois tout recuperer).
                je fait pareil pour tout les autres livres de la page
                    {si il y a plusieurs pages,}
                        je change de page et je retourne a l'etape des recuperation des information
                l'orsque tout a été fait
                    je cree mon CSV et
            je change de categorie
                je repete l'etapes jusqu'a plu de categories
        """
    list_books = []
    list_categorys = []
    list_categorys = get_categorys_link(url)
    for category in list_categorys:
        list_books = get_books_link(category)
        for book in list_books:
            print("DANS LE LIVRE" + book)
            create_file(book)


"""
        A FAIRE
        1 - REGLER LES LIENS DANS LA FONCTION GET CATEGORY LINK
        2 - FINIRE LA FONCTION MAIN QUI REGROUPE TOUS
        3 _ TROUVER UNE SOLUTION POUR REPONDRE AU DONNés VIDE COMME DESCRIPTION DANS LE CSV
"""
