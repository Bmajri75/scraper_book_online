# import du package requests, celui ci me permet de faire des requetes HTTP
import requests

# import de Bautifulsoup de bs4 pour recuperer les donner des fichier html ou XML
from bs4 import BeautifulSoup

# methode qui recupere le contenue d'une URL


def get_request_url(url):
    result = requests.get(url)
    return result.content


# Je fais appel a ma methode et je la parse dans la variable soup
url = "http://books.toscrape.com/catalogue/in-her-wake_980/index.html"
soup = BeautifulSoup(get_request_url(url), 'html.parser')


def get_text_from_page():
    # recupere la class price_color qui contien les prix des article
    informations = soup.find_all("tr")
    result = {}
    # je boucle pour cree un dictionaire des valeurs a recuper
    for information in informations:
        result.update({information.th.get_text(): information.td.get_text()})

# j'affiche le resultat
    print(result)


get_text_from_page()
