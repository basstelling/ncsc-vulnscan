from email.policy import default
from enum import unique
import time
import scrapy
# from requests import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from xss_scanner import get_form_details, submit_form, scan_xss

import os


class MySpider(CrawlSpider):
    name = 'webcrawler'
    allowed_domains = ['tynaarlo.nl']
    start_urls = ['http://localhost/Home_GemeenteTynaarlo.html']
    unique_urls = set()
    unique_forms = set()

    custom_settings = {
        'DEPTH_LIMIT': 1,
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
        hasForm = response.xpath("//form").get(default='not-found')
        iframe = response.xpath('//iframe/@src').get(default='not-found')
        # print(iframe)
        # print(hasForm, response.url)

        if iframe != 'not-found':
            iframe_url = str(self.start_urls[0] + iframe)
            # print(type(iframe_url))
            # print(iframe_url)
            yield scrapy.Request(iframe_url, callback = self.parse_iframe)

        if hasForm != 'not-found':
            if hasForm not in self.unique_forms:
                self.unique_forms.add(hasForm)
                self.unique_urls.add(response.url)

        

                # scan_xss(response.url, hasForm)
                with open('src\\data\\urls.txt','a+') as f:
                    f.write(f"{str(response.url)}\n")
                    print(response.url, hasForm)
        # else:
        #     pass

        # yield response.follow(url=link, callback=self.parse)

    def parse_iframe(self, response):
        # print(response)
        hasForm = response.xpath("//form").get(default='not-found')
        if hasForm != 'not-found':
            self.unique_urls.add(response.url)
            with open('src\\data\\urls.txt','a+') as f:
                f.write(f"{str(response.url)}\n")
        # print(hasForm)


if __name__ == "__main__":
    startTime = time.time()
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    totalTime = time.time() - startTime
    print("Webcrawling voltooid.")
    # print(f"Tijd: {(format(totalTime, ".2f"))} seconden"))