# coding: utf-8
""""""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import pickle
from os import path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yrttikanta.tables import Herb, Family, Base
from j24 import home


def create_herb(data):
    herb = Herb(name=data['Kasvi'], alt_names=data['Muut nimet'])
    herb.family = Family(name=data['Heimo'][0], name_fi=data['Heimo'][1])
    return herb


def data_gen_from_pkl(pkl_fpath):
    """generator from pickle"""
    with open(pkl_fpath, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


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
    ypkl = path.join(home(), 'koodi/yrttiharava/output/yrtit.pickle')
    ygen = data_gen_from_pkl(ypkl)
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    d = sample_data()
    vp = create_herb(d)
    session.add(vp)
