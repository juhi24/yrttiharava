# coding: utf-8
""""""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from yrttikanta.tables import Herb, Base


def sample_data():
    return {'Englanninkieliset nimet': ['Dead nettle'],
         'Heimo': ['Lamiaceae', 'Huulikukkaiskasvit'],
         'Kansanperinne': False,
         'Kasvi': 'Valkopeippi',
         'Kauppayrtti': False,
         'Latinankieliset nimet': ['Lamium album'],
         'Linkkitekstit': [''],
         'Muut nimet': ['Mukulvainen',
          'nuplukainen',
          'peippi',
          'peippo',
          'piikkiäinen',
          'piiskoheinä',
          'piitiäinen',
          'pillikka',
          'pillikäs',
          'porrinkainen',
          'porro',
          'sianleuka',
          'siannukulainen',
          'toukoruoho',
          'valkopeipponen',
          'valkopillike',
          'valkopillikäs'],
         'Ruotsinkieliset nimet': ['Vitplister'],
         'Saksankieliset nimet': ['Taubnessel'],
         'Vaikutusalueet rohtona': ['kuukautisvaivat', 'valkovuoto'],
         'Viljelytekniikka': False}


if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    d = sample_data()
    vp = Herb(name=d['Kasvi'])
    session.add(vp)
