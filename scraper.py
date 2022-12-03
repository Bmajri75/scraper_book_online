# import du package requests, celui ci me permet de faire des requetes HTTP
import requests
import csv
#  import de Bautifulsoup de bs4 pour recuperer les donner des fichier html ou XML
from bs4 import BeautifulSoup

# ici je recupere l'URL principal du site
url = "http://books.toscrape.com/index.html"


# Je crée une fonction qui me permet de recuperer la page HTML d'un lien
def get_request_url(url):
    result = requests.get(url)
    if result.ok:  # si le resultat est ok je retourne le contenue
        return result.content


# cette fonction permet de recupere tous les lien des categories
def get_all_category_link(url):
    all_link = []  # j'initialise une liste vide pour pouvoir stocké les liens
    soup = BeautifulSoup(get_request_url(url), 'html.parser')

# je boucle pour chaque lien  je les ajoute avec append
    for link in soup.find_all('a', href=True):
        all_link.append(link['href'])

    print(all_link)


get_all_category_link(url)


def get_text_from_page(url):
    # get_text_from_page fait appel a la fonction get_request_url
    soup = BeautifulSoup(get_request_url(url), 'html.parser')
    # recupere la class price_color qui contien les prix des article
    informations = soup.find_all("tr")
    result = {}
    # je boucle pour cree un dictionaire des valeurs a recuper
    for information in informations:
        result[information.th.get_text()] = information.td.get_text()
    return result


def create_file():
    # Je fais appel a ma methode
    url = "http://books.toscrape.com/catalogue/in-her-wake_980/index.html"
    details_of_my_book = get_text_from_page(url)

    en_tete = [details_of_my_book.keys()]
    corp_text = [details_of_my_book.values()]
    with open('data.csv', 'w') as fichier_csv:
        file_writer = csv.writer(fichier_csv)
        file_writer.writerows(en_tete)
        for en_tete in (en_tete):
            file_writer.writerows(corp_text)
