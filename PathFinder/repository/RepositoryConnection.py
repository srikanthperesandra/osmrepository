'''
Created on Feb 9, 2016

@author: srikanth
'''
from pymongo import MongoClient



class RepositoryConnection(object):
    _repository_instance = None
    def __init__(self,host,port,db):
        self.mongoClient = MongoClient(host, port)
        self.db = self.mongoClient[db]
    def getCollection(self,collection):
        return self.db[collection]
    def close(self):
        self.mongoClient.close()
    def getDB(self):
        return self.db
class RepositoryConnectionInstance(object):
    _repository_instance = None
    @staticmethod
    def getInstance(host,port,db):
        if __class__._repository_instance == None:
            __class__._repository_instance = RepositoryConnection(host,port,db)
        return __class__._repository_instance
        