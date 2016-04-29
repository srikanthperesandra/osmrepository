'''
Created on Apr 8, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbClusterEdges
from pfinder.PFinderConfig import dbClusterGraph
from services.entitiy.EntityService import EntityService
class ClusterGraphEntityService(object):
    def __init__(self):
        self.cGraphCollection = dbClusterGraph
        self.entityService = EntityService() 
    def addClusterGraphEdge(self,doc):
        self.entityService.addDocument(self.cGraphCollection, doc)
    def addClusterEdge(self,node):
        self.entityService.addDocument(dbClusterEdges, node)
    def getClusterEdges(self):
        return self.entityService.getAllDocuments(dbClusterEdges)
    def getClusterCenters(self):
        query ={"targetNodeCluster":{"$eq":None}}
        return self.entityService.getDocuments(dbClusterEdges,query)
    def isClusterCenter(self,osmId):
        query = {}
    def getClusterEdges2(self,targetNodeCluster):
        query ={"targetNodeCluster":{"$eq":targetNodeCluster}}
        return self.entityService.getDocuments(dbClusterEdges,query)
    def getStreetfromNode(self,nodeId):
        query = {"targetNode.osmId":nodeId}
        #print (query)
        return self.entityService.getDocument(dbClusterEdges, query)
        