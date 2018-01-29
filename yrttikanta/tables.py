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
    """the main herb class"""
    __tablename__ = 'herbs'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # many to one
    family_id = Column(Integer, ForeignKey('families.id'))
    family = relationship('Family', back_populates='herbs')
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


class Family(Base):
    """herb family in scientific classification"""
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    name_fi = Column(String)
    herbs = relationship('Herb', order_by=Herb.id, back_populates='family')

    def __repr__(self):
        return '<Family {}>'.format(self.name)

    @classmethod
    def get_or_create(cls, session, name, name_fi):
        # get the session cache, creating it if necessary
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        # create a key for memoizing
        key = (cls, name)
        # check the cache first
        o = cache.get(key)
        if o is None:
            # check the database if it's not in the cache
            o = session.query(cls).filter_by(name=name).first()
            if o is None:
                # create a new one if it's not in the database
                o = cls(name=name, name_fi=name_fi)
                session.add(o)
            # update the cache
            cache[key] = o
        return o


class AltName(Base):
    """Alternative herb names"""
    __tablename__ = 'alt_names'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=False) # TODO
    herbs = relationship('Herb',
                         secondary=herb_names,
                         back_populates='alt_names')

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<AltName {}>'.format(self.name)

