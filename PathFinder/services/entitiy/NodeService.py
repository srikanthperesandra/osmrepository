'''
Created on Feb 12, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbNodesCollection
from pfinder.PFinderConfig import dbHost
from pfinder.PFinderConfig import dbPort
from pfinder.PFinderConfig import dbRepository
from repository.RepositoryConnection import RepositoryConnectionInstance 
class NodeService:
    def __init__(self):
        self.repository = RepositoryConnectionInstance.getInstance(dbHost, dbPort,dbRepository)
        self.collection = self.repository.getCollection(dbNodesCollection)
    def getAllNodes(self):
        return self.collection.find()
    def getNode(self,osmId):
        return self.collection.find_one({"osmId":osmId})
           
