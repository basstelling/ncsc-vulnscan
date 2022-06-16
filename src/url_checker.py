from http import HTTPStatus
from urllib.parse import urlparse
import requests


def check_site_exist(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False
    except:
        return False

print(check_site_exist('https://nu.nl'))