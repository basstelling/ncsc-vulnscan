import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# alle forms binnen een website zoeken waarin XSS toegepast zou kunnen worden
def get_all_forms(url):
    forms = bs(requests.get(url).content, "html.parser")
    return forms.find_all("form")

def get_form_details(form):
    details = {}
    # form action ophalen
    action = form.attrs.get("action").lower()
    # form method ophalen ("GET", "POST", etc.)
    method = form.attrs.get("method", "get").lower()
    # input details ophalen
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    # alles in een bijbehorende dictionary stoppen
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    # volle url aanmaken
    target_url = urljoin(url, form_details["action"])
    # input ophalen van forms
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        # alle tekst vervangen en waarden zoeken met "value"
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            # als input_name en input_value bestaan, toevoegen aan form submission 
            data[input_name] = input_value

    # controleren op POST method
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        # controleren op GET method
        return requests.get(target_url, params=data)

def scan_xss(url):
    # alle forms binnen de URL ophalen dmv bovenstaande functie
    forms = get_all_forms(url)
    # print(forms)
    print(f"[+] {len(forms)} forms gevonden op {url}.")
    # meerdere soorten toevoegen -- mogelijk lezen vanuit .txt?
    js_script = "<Script>alert('test')</scripT>"
    # waarde teruggeven
    is_vulnerable = False
    # alle gevonden forms in de URL proberen
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS-kwetsbaarheid gevonden op {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    if is_vulnerable == False:
        print(f'[i] {url} is niet kwetsbaar voor XSS-scripting.')
        # return is_vulnerable

# demo
# scan_xss('https://www.martiniziekenhuis.nl')
# scan_xss('http://sudo.co.il/xss/level0.php')

# print(scan_xss('https://www.martiniziekenhuis.nl'))