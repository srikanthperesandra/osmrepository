'''
Created on Apr 1, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbCoordsCollection
from pfinder.PFinderConfig import dbHost
from pfinder.PFinderConfig import dbPort
from pfinder.PFinderConfig import dbRepository
from repository.RepositoryConnection import RepositoryConnectionInstance 
class CoordsService:
    def __init__(self):
        self.repository = RepositoryConnectionInstance.getInstance(dbHost, dbPort,dbRepository)
        self.collection = self.repository.getCollection(dbCoordsCollection)
    def getAllNodes(self):
        return self.collection.find()
    def getCoordinate(self,osmId):
        return self.collection.find_one({"osmId":osmId})
