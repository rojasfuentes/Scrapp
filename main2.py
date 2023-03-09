from threading import Thread
import requests
from bs4 import BeautifulSoup

DOMAIN = 'https://pokemondb.net'
URL = '/pokedex/all'


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        return soup
    else:
        print('Error: ', response.status_code)

def get_species_pokemon(url):
    soup = get_content(url)

    table = soup.find(
                'table', {'class': 'vitals-table'})
    species = table.tbody.find_all('tr')[2].td.text

    return species


if __name__ == '__main__':
    soup = get_content(DOMAIN + URL)

    table = soup.find('table', {'id': 'pokedex'})

    threads = []
    for row in table.find_all('tr')[1:15]:

        cols = row.find_all('td')

        name = cols[1].find('a').text
        type = [a.text for a in cols[2].find_all('a')]
        link = DOMAIN + cols[1].a['href']

        t = Thread(target=get_species_pokemon, args=(link,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
