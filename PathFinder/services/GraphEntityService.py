'''
Created on Mar 23, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbGraph
from services.entitiy.EntityService import EntityService
class GraphEntityService(object):
    def __init__(self):
        self.entityService = EntityService()
    def serialzeGraph(self,graph):
        self.entityService.addDocument(dbGraph, graph)
    def getGraph(self):
        return self.entityService.getAllDocuments(dbGraph)
    def getGraphEdges(self):
        query = {"edge":{"$ne":"null"}}
        return self.entityService.getDocuments(dbGraph, query)
    def getNodeEdges(self,osmId):
        query = {"edge":{"$ne":None},"from":osmId}
        #print (query)
        return self.entityService.getDocuments(dbGraph, query)
    def getNodebyOSMId(self,osmId):
        query = {"from":osmId}
        return self.entityService.getDocument(dbGraph, query)