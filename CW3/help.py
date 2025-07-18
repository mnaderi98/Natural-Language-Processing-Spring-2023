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
        for song in songs:
            music_name = song.attrib.get('data-title', '')
            album_name = song.attrib.get('data-album', '')
            artist_name =  song.attrib.get('data-artist', '')
            file_urls = song.attrib.get('data-src', '')