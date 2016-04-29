'''
Created on Apr 7, 2016

@author: srikanth
'''
from services.entitiy.EntityService import EntityService
import math
from random import random
from services.entitiy.CoordsService import CoordsService
from pfinder.PFinderConfig import INFINITY  , dbWaysCollection
from fsp.HaversianCalculator import Haversian
from fsp.Coordinates import Coordinates
from fsp.ClusterGraphEntityService import ClusterGraphEntityService
import pymongo
class ClusterGraph(object):
    def __init__(self,K):
        self.no_of_clusters = K
        self.clusters_center = [None]*K
        self.cluster_graph_collection = "cGraph_V1"
        self.clusters_collection = "cEdges_V1"
        self.entityService = EntityService()
        self.coodrdsService = CoordsService()
        self.cGraphService = ClusterGraphEntityService()
    def identifyClusters(self):
        N = self.entityService.getNumberOfDocuments("ways1")
        for i in range(0,self.no_of_clusters):            
            r = math.floor(random()*N)
            randomEdge = self.entityService.getRandomDocument("ways1", {}, r)
            edgeNode = randomEdge[0]['nodes'][0]
            edgeCoords =self.coodrdsService.getCoordinate(edgeNode)
            cEdgeNode = {}
            cEdgeNode['street'] = randomEdge[0]
            cEdgeNode['targetNode'] = edgeCoords
            self.entityService.addDocument(self.clusters_collection, cEdgeNode)
    def findMinEdgeNode(self,targetEdge,start_index,edges):
        minDist = INFINITY
        #query = {"from.osmId":{"$eq":osmId}}
        targetNodeCoords = targetEdge['targetNode']#self.entityService.getDocument("graph2", query)['from']
        #print(targetNodeCoords)
        minFirstNodeCoords = None
        for i in range(start_index,edges.count()):            
            firstNode = edges[i]['targetNode']
            if edges[i]['street']['osmId']!=targetEdge['street']['osmId']: 
                dist = Haversian.getInstance().calculateDistance(Coordinates(firstNode['lng'],firstNode['lat']),Coordinates(targetNodeCoords['lng'],targetNodeCoords['lat']))
                if dist < minDist:
                    minDist = dist
                    minFirstNodeCoords= firstNode
        
        result = {}
        result['from'] = targetNodeCoords
        result ['to'] = minFirstNodeCoords
        result['distance'] = minDist
        return result
        #print (minDist)
        
        #print (graphNode)
        
    def addGraphEdge(self,targetNodeCoords,minFirstNodeCoords,minDist):
        graphNode = {}
        #graphNode['index']=(counter-1,index)
        graphNode['from'] = targetNodeCoords
        graphNode['to'] = minFirstNodeCoords
        #graphNode['edge']= nodesEdge
        graphNode['dist']=minDist 
        #print (graphNode)
        #self.entityService.addDocument(self.cluster_graph_collection, graphNode)
        self.cGraphService.addClusterGraphEdge(graphNode)
        graphNode = {}
        #graphNode['index']=(index,counter-1)
        graphNode['from'] = minFirstNodeCoords
        graphNode['to'] = targetNodeCoords
        graphNode['dist']=minDist
        self.cGraphService.addClusterGraphEdge(graphNode)
        #self.entityService.addDocument(self.cluster_graph_collection, graphNode)
    def connectClusters(self):
        streets = self.entityService.getAllDocuments(self.clusters_collection)
        for i in range(0,streets.count()-1):
            node = self.findMinEdgeNode(streets[i], (i+1),streets)#processedEdges)
            #node = self.findMinEdgeNode(streets[i], 0,streets)#processedEdges)
            self.addGraphEdge(node['from'], node['to'], node['distance'])
    
            
            #processedEdges.remove(street)
    def performEdgeClustering(self):
        cluster_centers = self.cGraphService.getClusterCenters()
        cluster_centers_copy = cluster_centers.clone()
        print(cluster_centers.count())
        streets = self.entityService.getAllDocuments(dbWaysCollection)
        for i in range(0,10):
            if self.isClusterCenter(streets[i]['osmId'], cluster_centers_copy):
                print ("Encountered cluster center, skipping cluster assignment")
                continue
            targetEdge={}
            targetEdge['street']=streets[i]#self.entityService.getDocument("graph2",{"from.osmId":{"$eq":streets[i]['nodes'][0]}})
            tempNode = self.entityService.getDocument("graph2",{"from.osmId":{"$eq":streets[i]['nodes'][0]}})
            if tempNode == None:
                tempNode = self.coodrdsService.getCoordinate(streets[i]['nodes'][0])
            else:
                tempNode = tempNode['from']
            targetEdge['targetNode'] = tempNode
            targetEdge['targetNodeCluster'] = self.findMinEdgeNode(targetEdge, 0, cluster_centers)['to']['osmId']
            self.cGraphService.addClusterEdge(targetEdge)
    
    def connectEdgeswithInClusters(self):
        cluster_centers = self.cGraphService.getClusterCenters()
        for i in range (0,cluster_centers.count()):
            cluster_edges = self.cGraphService.getClusterEdges2(cluster_centers[i]['targetNode']['osmId'])
            if (cluster_edges.count()==0):
                print ("skipping edge cluster connection, no edge exists in cluster")
                continue
            for j in range(0,cluster_edges.count()-1):
                node = self.findMinEdgeNode(cluster_edges[j], (j+1),cluster_edges)
                #node = self.findMinEdgeNode(cluster_edges[j], 0,cluster_edges)
                self.addGraphEdge(node['from'], node['to'], node['distance'])
                #print (node)
            node =self.findMinEdgeNode(cluster_centers[i], 0, cluster_edges)
            self.addGraphEdge(node['from'], node['to'], node['distance'])
            #print ("--------------------------")
    def isClusterCenter(self,osmId,centers):
            return any(obj['street']['osmId']==osmId for obj in centers)
def tester():
    cg = ClusterGraph(60)
    #cg.identifyClusters()
    #cg.connectClusters()
    #cg.performEdgeClustering()
    cg.connectEdgeswithInClusters()
tester()
            