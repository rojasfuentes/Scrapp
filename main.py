import requests
from bs4 import BeautifulSoup
import threading

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


def process_pokemon(row):
    cols = row.find_all('td')

    name = cols[1].find('a').text
    type = [a.text for a in cols[2].find_all('a')]
    link = DOMAIN + cols[1].a['href']

    species = get_species_pokemon(link)

    print(name, '', type, '-', species)


def process_rows(rows):
    threads = []
    for row in rows:
        thread = threading.Thread(target=process_pokemon, args=(row,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    soup = get_content(DOMAIN + URL)

    table = soup.find('table', {'id': 'pokedex'})

    # Dividing the table rows in smaller chunks for processing
    rows_chunks = [table.find_all('tr')[i:i+5]
                   for i in range(1, len(table.find_all('tr')), 5)]

    # Process rows chunks in parallel
    for chunk in rows_chunks:
        process_rows(chunk)
