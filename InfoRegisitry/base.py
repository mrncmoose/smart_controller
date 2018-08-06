'''
Created on Aug 5, 2018

@author: moose
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class MyClass(object):
    '''
    classdocs
    '''
# coding=utf-8

engine = create_engine('postgresql://mooseGre:Mo%902ose@localhost:54320/sqlalchemy')
Session = sessionmaker(bind=engine)

Base = declarative_base()