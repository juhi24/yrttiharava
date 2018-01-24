# coding: utf-8
""""""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()
herb_names = Table('herb_names', Base.metadata,
                   Column('herb_id', ForeignKey('herbs.id'), primary_key=True),
                   Column('name_id', ForeignKey('alt_names.id'), primary_key=True))


class Herb(Base):
    __tablename__ = 'herbs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # many to many
    alt_names = relationship('AltName',
                             secondary=herb_names,
                             back_populates='herbs')

    def __init__(self, name, alt_names=None):
        self.name = name
        if alt_names is not None:
            for alt_name in alt_names:
                self.alt_names.append(AltName(alt_name))


    def __repr__(self):
        return '<Herb {}>'.format(self.name)


class AltName(Base):
    """Alternative herb names"""
    __tablename__ = 'alt_names'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    herbs = relationship('Herb',
                         secondary=herb_names,
                         back_populates='alt_names')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<AltName {}>'.format(self.name)

