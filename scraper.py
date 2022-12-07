# import du package requests, celui ci me permet de faire des requetes HTTP
import requests
import csv
#  import de Bautifulsoup de bs4 pour recuperer les donner des fichier html ou XML
from bs4 import BeautifulSoup
# ici je recupere l'URL principal du site
url = "http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html"


# recupere la requete sur URL en parametre
def get_request_url(url):
    response = requests.get(url)
    if response.ok:  # si le resultat est ok je retourne le contenue
        return response.text

# cette fonction permet de recupere tous les lien des categorie et des livres
# def get_all_link(url):
#     book_link = []  # j'initialise une liste vide pour pouvoir stocké les liens des livres
#     category_link = []  # j'initialise une liste pour les category
#     all_link = []
#     soup = BeautifulSoup(get_request_url(
#         url), 'html.parser')  # je cree ma soupe
# # je boucle et pour chaque lien  je le rajoute a book_link qui va contenir tout les liens dans un premier temps
#     for link in soup.find_all('a', href=True):
#         book_link.append(link['href'])

# # je recupere tout les liens qui contienne les categorie je les ajoutes dans la liste categorie
# # et je les supprime de book_link
#     for link in book_link:
#         if ("catalogue/category/books/" in link):
#             category_link.append(link)
#             book_link.remove(link)

#     all_link = [category_link, book_link]
#     print(all_link[1])

# cette fonctions automatise les sortie des liens et les changement de pages

        # get_text_from_page fait appel a la fonction get_request_url


def get_informations_from_page(url):
    informations = []

    soup = BeautifulSoup(get_request_url(url), 'html.parser')
    # recuperer les information sous forme de dictionary :

    # recupere les informations dans les <td> c'est à dire
    """
    ● universal_ product_code (upc)
    ● price_including_tax
    ● price_excluding_tax
    ● number_available
    ● review_rating

    """
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

    """
    je boucle pour cree un dictionaire des valeurs a recuper
    ● product_page_url
    ● title
    ● product_description
    ● category
    ● image_url
    """
    # for information in informations:
    #     informations[information.th.get_text()] = information.td.get_text()
    # return information


# cette fonction me permet de cree un fichier csv
def create_file(url):
    # Je fais appel a ma fonction pour recupere mes informations de la page
    details_of_my_book = get_informations_from_page(url)
    en_tete = ["Product_page_url", "upc", "Title", "Price_including_tax", "Price_excluding_tax",
               "Pumber_available", "Product_description", "Category", "Review_rating", "Image_url"]

    with open('data.csv', 'w') as fichier_csv:
        file_writer = csv.writer(fichier_csv)
        file_writer.writerow(en_tete)
        file_writer.writerow(details_of_my_book)


create_file(url)
