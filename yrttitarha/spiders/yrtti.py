# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import scrapy


def ll2dict(ll):
    """List of lists to dict. 1st item of each sublist is the key."""
    d = {}
    for l in ll:
        key = l[0]
        if key.lower() == 'kasvi':
            d[key] = l[1]
            continue
        try:
            if len(l[1:]) > 1:
                raise ValueError
            d[key] = bool(int(l[-1]))
        except ValueError:
            d[key] = l[1:]
    d.pop('', None) # remove empty key, if exists
    return d


def parse_tiedot(s):
    """tiedot string to dict"""
    l = s.split('\n')
    ll = [s.split('|') for s in l]
    d = ll2dict(ll)
    return d


class YrttiSpider(scrapy.Spider):
    """for crawling and parsing all herbs in yrttitarha"""
    name = 'yrtti'
    allowed_domains = ['yrttitarha.fi']
    start_urls = ['http://yrttitarha.fi/kanta/haku.cgi?hakusanat=kaikki-suomi']

    def parse(self, response):
        """Follow links to data on each herb and call parsers."""
        # unique /kanta/urls
        hrefs = set(response.css('a::attr(href)').extract())
        for href in hrefs:
            # /kanta/name/
            yield response.follow(href, callback=self.parse_yrtti)
            # /kanta/name/tiedot
            yield response.follow(href+'tiedot', callback=self.parse_tiedot)

    def parse_yrtti(self, response):
        """parse descriptions"""
        # TODO: parse descriptions
        yield {'name': response.css('h1::text').extract_first()}

    def parse_tiedot(self, response):
        """parse_tiedot wrapper"""
        yield parse_tiedot(response.text)


