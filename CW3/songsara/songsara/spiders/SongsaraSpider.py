import json
from pathlib import Path

import jmespath
from scrapy.crawler import CrawlerProcess
import scrapy
import pandas as pd


class SongsrarSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://songsara.net/117281/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        Path(filename).write_bytes(response.body)
        self.log(f'Saved file {filename}')
        self.parse_post(response)

    def parse_post(self, response):
        """
        Parses a post page
        """
        if len(response.css(
                '.dl-box')) > 1:  # our spider does not support such pages with multiple music tracks like https://tinyurl.com/2p85b4hx
            return []

        schema_graph_data = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').get())
        info = jmespath.search('"@graph"[?"@type"==\'Article\']|[0]', schema_graph_data)
        if info:
            songs = response.xpath('//ul[has-class("audioplayer-audios")]//li')
            artists = response.xpath('//div[has-class("AR-Si")]//a')
            music_names = []
            album_names = []
            artist_names = []
            file_urls = []
            for song in songs:
                music_names.append(song.attrib.get('data-title', ''))
                album_names.append(song.attrib.get('data-album', ''))
                artist_names.append(song.attrib.get('data-artist', ''))
                file_urls.append(song.attrib.get('data-src', ''))
            csv_dat = {'music_name': music_names,
                        'album_name': album_names,
                        'artist_name': artist_names,
                        'file_url': file_urls}

            df = pd.DataFrame(csv_dat, columns=['music_name', 'album_name', 'artist_name', 'file_url'])
            df.to_csv('musics_data.csv', index=False)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(SongsrarSpider)
process.start()
