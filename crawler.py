from pathlib import Path
import queue
import requests
from bs4 import BeautifulSoup
import time

import requests
from bs4 import BeautifulSoup
 

base_url = 'http://localhost'
resp = requests.get(base_url)
soup = BeautifulSoup(resp.text, 'html.parser')
urls = []

for link in soup.find_all('a'):
    if link.get('href').startswith('/'):
        urls.append(base_url + str(link.get('href')))
    elif link.get('href').startswith(base_url):
        urls.append(link.get('href'))



# for url in urls:
#     resp = requests.get(url)
#     # time.sleep(1)
#     deep_soup = BeautifulSoup(resp.text, "html.parser")
#     for a in deep_soup.find_all('a'):
#         # print(a.get('href'))
#         if a.get('href') is not None:
#             if a.get('href').startswith('/'):
#                 urls.append(url + (str(a.get('href'))))
#             elif a.get('href').startswith(base_url):
#                 urls.append(a.get('href'))

# duplicates verwijderen uit de list
urls = list(set(urls))

    # for link in urls:
    #     resp = requests.get(link)
    #     deep_soup = BeautifulSoup(resp.text, "html.parser")
    #     for a in deep_soup.find_all('a'):
    #         if a.get('href').startswith('/'):
    #             urls.append(url + str(a) + str(a.get('href')))
    #         elif a.get('href').startswith(url + str(a)):
    #             urls.append(a.get('href'))
        # for url in urls:
        #     resp = requests.get(url)

    # if (link.get('href')).startswith('/'):
    #     url = url + str(link.get('href'))
    #     urls.append(url)
        # print(url, "\n")

for url in urls:
    print(url)
print(len(urls))

# def crawl(base_url, start_anchor):
#     search_anchors = queue.Queue()
#     urls = []
#     while True:
#         headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' }
#         response = requests.request('GET', base_url + start_anchor, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
#         anchors = find_local_anchors(soup, start_anchor)
#         if anchors:
#             for a in anchors:
#                 url = base_url + a
#                 time.sleep(1)
#                 if url in urls:
#                     continue
#                 if not Path(a).suffix:
#                     search_anchors.put(a)
#                 urls.append(a)
#                 print(url)

#         if search_anchors.empty():
#             break
#         start_anchor = search_anchors.get()
#     return urls

# def find_local_anchors(soup, start_anchor):
#     anchors = []
#     for link in soup.find_all('a'):
#         if "href" in link.attrs:
#             anchor = link.attrs["href"]
#         if anchor.startswith(start_anchor):
#             anchors.append(anchor)
#     return anchors