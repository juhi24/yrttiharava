# coding: utf-8
import scrapy


def ll2dict(ll):
    """List of lists to dict. 1st item of each sublist is the key."""
    d = {}
    for l in ll:
        d[l[0]] = l[1:]
    return d


class YrttiSpider(scrapy.Spider):
    name = 'yrtti'
    allowed_domains = ['yrttitarha.fi']
    start_urls = ['http://yrttitarha.fi/kanta/haku.cgi?hakusanat=kaikki-suomi']

    def parse(self, response):
        # unique /kanta/urls
        hrefs = set(response.css('a::attr(href)').extract())
        for href in hrefs:
            # /kanta/name/
            yield response.follow(href, callback=self.parse_yrtti)
            # /kanta/name/tiedot
            yield response.follot(href+'tiedot', callback=self.parse_tiedot)

    def parse_yrtti(self, response):
        yield {'name': response.css('h1::text').extract_first()}

    def parse_tiedot(self, response):
        l = response.text.split('\n')
        ll = [s.split('|') for s in l]
        d = ll2dict(ll)


