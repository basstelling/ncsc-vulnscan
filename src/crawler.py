import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

import os


class MySpider(CrawlSpider):
    name = 'webcrawler'
    allowed_domains = ['tynaarlo.nl']
    start_urls = ['https://www.tynaarlo.nl/']

    custom_settings = {
        'DEPTH_LIMIT': 1,
        'CONCURRENT_REQUESTS': 10,
        'ROBOTSTXT_OBEY': False,
        'REACTOR_THREADPOOL_MAXSIZE': 400,
        'LOG_LEVEL': 'INFO',
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE' :'scrapy.squeues.FifoMemoryQueue'
    }

    try:
        os.remove('src\\crawler_data\\urls.txt')
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
        for link in self.link_extractor.extract_links(response):
            # hasForm = response.xpath("//form").extract_first(default='not-found')
            # if hasForm != 'not-found':
            with open('src\\crawler_data\\urls.txt','a+') as f:
                f.write(f"{str(link)}\n")

            yield response.follow(url=link, callback=self.parse)

if __name__ == "__main__":
    startTime = time.time()
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    totalTime = time.time() - startTime
    print("Webcrawling voltooid.")
    print("Tijd: ", format(totalTime, ".2f"))