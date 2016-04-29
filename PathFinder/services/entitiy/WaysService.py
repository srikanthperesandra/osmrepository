'''
Created on Mar 26, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbWaysCollection
from pfinder.PFinderConfig import dbHost
from pfinder.PFinderConfig import dbPort
from pfinder.PFinderConfig import dbRepository
from repository.RepositoryConnection import RepositoryConnectionInstance 

class WayService(object):
    def __init__(self):
        self.repository = RepositoryConnectionInstance.getInstance(dbHost, dbPort,dbRepository)
        self.collection = self.repository.getCollection(dbWaysCollection)
    def getAllWays(self):
        return self.collection.find()
    def fetchWayforNodes(self,nodes):
        #print (nodes)
        return self.collection.find({"nodes":{"$all":nodes}},{"_id":0,"osmId":1})