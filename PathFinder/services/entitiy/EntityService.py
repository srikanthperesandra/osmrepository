'''
Created on Mar 23, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbHost
from pfinder.PFinderConfig import dbPort
from pfinder.PFinderConfig import dbRepository
from repository.RepositoryConnection import RepositoryConnectionInstance 
class EntityService:
    def __init__(self):
        self.repository = RepositoryConnectionInstance.getInstance(dbHost, dbPort,dbRepository)
    def getAllDocuments(self,collection):
        #print (collection)
        return self.repository.getCollection(collection).find()
    def addDocument(self,collection,document):
        self.repository.getCollection(collection).insert(document,True)
    def addDocuments(self,collection,documents):
        self.repository.getCollection(collection).insert_many(documents)    
    def getDocuments(self,collection,query):
        return self.repository.getCollection(collection).find(query)
    def getDocument(self,collection,query):
        #print (query)
        return self.repository.getCollection(collection).find_one(query)
    def getNumberOfDocuments(self,collection):
        return self.repository.getCollection(collection).count()
    def getRandomDocument(self,collection,query,r):
        return self.repository.getCollection(collection).find().limit(1).skip(r)
    def getDistinctDocuments(self,collection,attr):
        return self.repository.getCollection(collection).distinct(attr)
    def getDocuments2(self,collection,query,attributesExclusion):
        return self.repository.getCollection(collection).find(query,attributesExclusion)
    def runCommand(self,command):
        return self.repository.getDB().command(command)    