# coding: utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import scrapy
import requests
from bs4 import BeautifulSoup


def ll2dict(ll):
    """List of lists to dict. 1st item of each sublist is the key."""
    d = {}
    for l in ll:
        key = l[0]
        if key == 'kasvi': # herb name
            d[key] = l[1]
            continue
        values = l[1:]
        try:
            if len(values) != 1:
                raise ValueError
            d[key] = bool(int(values[0]))
        except ValueError:
            try:
                values.remove('')
            except ValueError:
                pass # everything is ok
            d[key] = values
    d.pop('', None) # remove empty key, if exists
    return d


def parse_tiedot(s):
    """tiedot string to dict"""
    l = s.lower().split('\n')
    ll = []
    for ss in l:
        inner_l = ss.split('|')
        ll.append([sss.strip() for sss in inner_l])
    d = ll2dict(ll)
    return d


def parse_texts(response):
    soup = BeautifulSoup(response.text, 'lxml')
    sections = {}
    for t in ('a', 'b', 'i'):
        for tag in soup.find_all(t):
            tag.replace_with_children()
    for h2 in soup.find_all('h2'):
        if h2.parent.name == 'p':
            h2.parent.replace_with_children()
        p_texts = []
        for s in h2.next_siblings:
            if s.name == 'h2':
                break
            if hasattr(s, 'descendants'):
                br = False
                for d in s.descendants:
                    if d.name == 'h2':
                        br = True
                if br:
                    break
            if hasattr(s, 'text'):
                text = s.text.replace('\n', '')
                if text and text not in ['Ruokaohjeet']:
                    p_texts.append(text)
        sections[h2.text] = p_texts or [h2.next_sibling.replace('\n', '')]
    return sections


def parse_texts2(response):
    """parse to {header: string, ...} pairs keeping most tags"""
    soup = BeautifulSoup(response.text, 'lxml')
    sections = {}
    for t in ('a',):# 'b', 'i'):
        for tag in soup.find_all(t):
            tag.replace_with_children()
    for h2 in soup.find_all('h2'):
        if h2.parent.name == 'p':
            h2.parent.replace_with_children()
    for h2 in soup.find_all('h2'):
        texts = []
        for s in h2.next_siblings:
            if s.name == 'h2':
                break
            if hasattr(s, 'text'):
                if s.text in ('', '\n'):
                    continue
                con = False
                for extra in ['Kansanperinne', 'Viljelyohjeet', 'Kauppayrtti',
                              'Ruokaohjeet', 'Ravintoainesisältö']:
                    if extra in s.descendants:
                        con = True
                if con:
                    continue
            elif s.strip()=='':
                continue
            texts.append(str(s).replace('\n', ''))
        sections[h2.text] = ''.join(texts) or h2.next_sibling.replace('\n', '')
    return sections


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
            yield response.follow(href, callback=self.parse_tiedot)

    def parse_tiedot(self, response):
        """parse_tiedot wrapper"""
        subresponse = requests.get(response.urljoin('tiedot'))
        data = parse_tiedot(subresponse.text)
        data['sections'] = parse_texts2(response)
        yield data
