# -*- coding: utf-8 -*-
import scrapy


class YrttiSpider(scrapy.Spider):
    name = 'yrtti'
    allowed_domains = ['yrttitarha.fi']
    start_urls = ['http://yrttitarha.fi/kanta/haku.cgi?hakusanat=kaikki-suomi']

    def parse(self, response):
        hrefs = set(response.css('a::attr(href)').extract())
        for href in hrefs:
            yield response.follow(href, callback=self.parse_yrtti)

    def parse_yrtti(self, response):
        yield {'name': response.css('h1::text').extract_first()}
