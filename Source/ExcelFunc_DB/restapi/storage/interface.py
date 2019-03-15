"""
Created on Nov 18, 2014
@author: xieyi

"""

from database import *


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


@singleton
class StorageIF(object):
    def __init__(self):
        self._storage = PostgresDataBase()


    def get_index(self, _id ):
        """
         test
        """
        return self._storage.get_index(_id)
    
      
