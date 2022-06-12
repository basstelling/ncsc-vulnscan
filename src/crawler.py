from email.policy import default
from enum import unique
import pprint
import time
from urllib.parse import urljoin
import bs4
import requests
import scrapy
# from requests import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from xss_scanner import get_all_forms, get_form_details, submit_form, scan_xss

import os


class MySpider(CrawlSpider):
    name = 'webcrawler'
    # readshopeelde.nl
    # https://www.readshopeelde.nl/

    # tynaarlo.nl
    # http://localhost/Home_GemeenteTynaarlo.html
    allowed_domains = ['tynaarlo.nl']
    start_urls = ['http://localhost/Home_GemeenteTynaarlo.html']
    unique_urls = set()
    unique_forms = set()

    custom_settings = {
        # 'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS': 100,
        'ROBOTSTXT_OBEY': False,
        'REACTOR_THREADPOOL_MAXSIZE': 400,
        'LOG_LEVEL': 'INFO',
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE' :'scrapy.squeues.FifoMemoryQueue',
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    }

    try:
        os.remove('src\\data\\urls.txt')
    except OSError:
        pass

    rules = (
        # Extract and follow all links!
        Rule(LinkExtractor(), callback='parse', follow=True),
    )

    def __init__(self, *a, **kw):
        super(MySpider, self).__init__(*a, **kw)
        self.link_extractor = LinkExtractor(allow_domains=self.allowed_domains, unique=True)

    def parse(self, response):
        # print(response.url)
        hasForm = response.xpath("//form").get(default='form-not-found')
        iframe = response.xpath('//iframe/@src').get(default='iframe-not-found')
        # print(iframe, hasForm, response.url)
        # # print(hasForm, response.url)

        if iframe != 'iframe-not-found':
            iframe_url = str(self.start_urls[0] + iframe)
            print(iframe_url)

        if hasForm != 'form-not-found':
            xss = scan_xss(response.url)
            with open('src\\data\\urls.txt','a+') as f:
                f.write(f"{str(response.url)} = {xss}\n")

        # if hasForm == 'form-not-found':
        #     print(hasForm, iframe, response.url)
        # else: 
        #     print(hasForm, iframe, response.url)
        # with open('src\\data\\urls.txt','a+') as f:
        #     f.write(f"{str(response.url)}\n")


        # if iframe != 'not-found':
        #     iframe_url = str(self.start_urls[0] + iframe)
        #     with open('src\\data\\urls.txt','a+') as f:
        #         f.write(f"{str(iframe_url)}\n")
        #     # print(type(iframe_url))
        #     print(iframe_url)
        #     # yield scrapy.Request(iframe_url, callback = self.parse_iframe)

        # if hasForm != 'not-found':
        #     if hasForm not in self.unique_forms:
        #         self.unique_forms.add(hasForm)
        #         self.unique_urls.add(response.url)

        #         # scan_xss(response.url, hasForm)
        #         with open('src\\data\\urls.txt','a+') as f:
        #             f.write(f"{str(response.url)}\n")
        #             print(response.url, hasForm)
        # else:
        #     pass

        yield response.follow(url=response.url, callback=self.parse)
    # def parse_iframe(self, response):
    #     # print(response)
    #     hasForm = response.xpath("//form").get(default='not-found')
    #     if hasForm != 'not-found':
    #         self.unique_urls.add(response.url)
    #         with open('src\\data\\urls.txt','a+') as f:
    #             f.write(f"{str(response.url)}\n")
    #             print(response.url, hasForm)
        # print(hasForm)

    # def parse(self, response):
    #     # print(response.url)
    #     hasForm = response.xpath("//form").get(default='not-found')
    #     iframe = response.xpath('//iframe/@src').get(default='not-found')
    #     print(hasForm, iframe, response.url)

    #     if iframe != 'not-found':
    #         iframe_url = str(self.start_urls[0] + iframe)
    #         # print(iframe_url, iframe, self.start_urls)
    #         print(scan_xss(iframe_url, hasForm))
    #         self.unique_urls.add(iframe_url)
    #         # yield scrapy.Request(iframe_url, callback = self.parse_iframe)

    #     if hasForm != 'not-found':
    #         xss = scan_xss(response.url, hasForm)
    #         print(xss)
    #         self.unique_urls.add(response.url)
    #         self.unique_forms.add(hasForm)

        # for url in self.unique_urls:
        #     for form in 


        # print(iframe)
        # print(hasForm, response.url)

        # if iframe != 'not-found':
        #     iframe_url = str(self.start_urls[0] + iframe)
        #     # print(type(iframe_url))
        #     print(iframe_url)
        #     yield scrapy.Request(iframe_url, callback = self.parse_iframe)

        # if hasForm != 'not-found':
        #     if hasForm not in self.unique_forms:
        #         self.unique_forms.add(hasForm)
        #         self.unique_urls.add(response.url)
        #         xss = scan_xss(response.url, hasForm)
        #         with open('src\\data\\urls.txt','a+') as f:
        #             f.write(f"{str(response.url)} + {xss}\n")
        #             print(response.url, hasForm, "\n")
        # else:
        #     pass

        # yield response.follow(url=link, callback=self.parse)

    # def parse_iframe(self, response):

        # print(response)
        # hasForm = response.xpath("//form").get(default='not-found')
        # if hasForm != 'not-found':
        #     self.unique_urls.add(response.url)
        #     xss = scan_xss(response.url, hasForm)
        #     print(xss)
        #     with open('src\\data\\urls.txt','a+') as f:
        #         f.write(f"{str(response.url)} + {xss}\n")
        # print(hasForm)

    def get_all_forms(url):
        forms = bs4(requests.get(url).content, "html.parser")
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
        # for url in form_ur
        forms_on_page = get_all_forms(url)
        # print(forms)
        print(f"[+] {len(forms_on_page)} forms gevonden op {url}")
        # meerdere soorten toevoegen -- mogelijk meerdere vectors lezen vanuit .txt
        # <b onmouseover=alert('Wufff!')>click me!</b> @ https://xss-game.appspot.com/level2
        js_script = "<Script>alert('test')</scripT>"
        # waarde teruggeven
        is_vulnerable = False
        # alle gevonden forms in de URL proberen
        for form in forms_on_page:
            form_details = get_form_details(form)
            content = submit_form(form_details, url, js_script).content.decode()
            if js_script in content:
                print(f"[+] XSS-kwetsbaarheid gevonden op {url}")
                print(f"[*] Form details:")
                pprint(form_details)
                is_vulnerable = True
        if is_vulnerable == False:
            print(f'[i] {url} is niet kwetsbaar voor XSS-scripting.')
            return is_vulnerable


if __name__ == "__main__":
    startTime = time.time()
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    totalTime = time.time() - startTime
    print("Webcrawling voltooid.")
    # print(f"Tijd: {(format(totalTime, ".2f"))} seconden"))