from pathlib import Path
from scrapy.crawler import CrawlerProcess
import scrapy


class SongsrarSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://songsara.net/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(SongsrarSpider)
process.start()
