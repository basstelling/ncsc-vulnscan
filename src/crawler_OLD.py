from pathlib import Path
import queue
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import threading
import concurrent.futures
import requests
from bs4 import BeautifulSoup
 
base_url = 'http://localhost/Home_GemeenteTynaarlo.html'

# localhost_base vervangen met base_url voor live versie!
localhost_base = 'https://www.tynaarlo.nl'

def crawler(base_url):
    startTime = time.time()
    urls = []
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)
    for link in soup.find_all('a'):
        # print(link)
        if link.get('href').startswith('/'):
            # print(link.get('href').startswith('/'))
            urls.append(localhost_base + str(link.get('href')))
        elif link.get('href').startswith(localhost_base):
            urls.append(link.get('href'))

    # duplicates verwijderen uit de list
    urls = list(set(urls))

    # rest van de urls ophalen
    for deep_url in urls:
        deep_resp = requests.get(deep_url)
        try:
            deep_soup = BeautifulSoup(deep_resp.text, "html.parser")
            for deep_link in deep_soup.find_all('a'):
                if str(deep_link.get('href')).startswith('/'):
                    # print(deep_link.get('href'))
                    if localhost_base + str(deep_link.get('href')) not in urls:
                        urls.append(localhost_base + str(deep_link.get('href')))
                        print(deep_link.get('href'))
                    else:
                        continue

        except (TypeError, UserWarning) as e:
            print(e)


    # return urls
    for url in urls:
        print(url)
    totalTime = time.time() - startTime
    print(f'Gevonden websites: {len(urls)}')
    print(f'Totale tijd: {format(totalTime, ".2f")}')
    # print(f'Extra website: {deep_url}')



# crawler(base_url)
