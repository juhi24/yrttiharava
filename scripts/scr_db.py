# coding: utf-8
""""""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Herb(Base):
    __tablename__ = 'herbs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return '<Herb {}>'.format(self.name)


class HerbName(Base):
    """relational link between herbs and their alternative names"""
    __tablename__ = 'herb_names'
    
    herb_id = Column(Integer)
    name_id = Column(Integer)


class AltName(Base):
    """Alternative herb names"""
    __tablename__ = 'alt_names'

    id = Column(Integer, primary_key=True)
    name = Column(String)



