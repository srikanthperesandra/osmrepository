'''
Created on Mar 15, 2016

@author: srikanth
'''
from services.entitiy.NodeService import NodeService
from HaversianCalculator import Haversian
from Coordinates import Coordinates
from services.GraphEntityService import GraphEntityService
from services.entitiy.WaysService import WayService

class Graph(object):
    def __init__(self):
        self.graph = {}
        self.vertices = []
        self.nodeService = NodeService()
        self.graphService = GraphEntityService()
        self.wayService = WayService()
    def readVertices(self):
        nodes=self.nodeService.getAllNodes()
        for i in range(0,nodes.count()):
            for j in range(0,nodes.count()):
                nodesEdge = None
                if i==j:
                    self.graph[i,j] = 0
                else:
                    edge = self.wayService.fetchWayforNodes([nodes[i]['osmId'],nodes[j]['osmId']])
                    if edge!= None and edge.count()>0 and 'osmId' in edge[0]:
                        nodesEdge = edge[0]
                    self.graph[i,j] =  Haversian.getInstance().calculateDistance(Coordinates(nodes[i]['lng'],nodes[i]['lat']),Coordinates(nodes[j]['lng'],nodes[j]['lat']))
                graphNode = {}
                graphNode['index']=(i,j)
                graphNode['from'] = nodes[i]['osmId']
                graphNode['to'] = nodes[j]['osmId']
                graphNode['distance'] = self.graph[i,j]
                graphNode['edge']= nodesEdge
                self.storeGraph(graphNode)
    def getGraph(self):
        return self.graph                
    def storeGraph(self,graphNode):
        self.graphService.serialzeGraph(graphNode)

def tester():
    g = Graph()
    g.readVertices()
tester()
        