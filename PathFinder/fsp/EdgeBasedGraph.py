
'''
@author: srikanth
'''
from services.GraphEntityService import GraphEntityService
from services.entitiy.EntityService import EntityService
from pfinder.PFinderConfig import dbWaysCollection, INFINITY
from fsp.HaversianCalculator import Haversian
from services.entitiy.CoordsService import CoordsService
from fsp.Coordinates import Coordinates
class EdgeBasedGraph(object):
    def __init__(self):
        self.entityService = EntityService()
        self.waysCollection = dbWaysCollection
        self.coordsService = CoordsService()
    def parseEdgesForConnectivity(self):
        edges=self.entityService.getAllDocuments(self.waysCollection)
        counter = 0
        for i in range(0,100):
            tempNodes = edges[i]['nodes']
            #self.calculateHaversian(edges[i],tempNodes,counter)
            counter=counter+len(tempNodes)
            self.findMinEdgeNode(i,tempNodes[len(tempNodes)-1],edges,counter,100)
    def calculateHaversian(self,nodesEdge,nodes,counter):
        for i in range(0,len(nodes)-1):
            fromNode = self.coordsService.getCoordinate(nodes[i])
            toNode = self.coordsService.getCoordinate(nodes[i+1])
            dist=Haversian.getInstance().calculateDistance(Coordinates(fromNode['lng'],fromNode['lat']),Coordinates(toNode['lng'],toNode['lat']))
            graphNode = {}
            graphNode['index']=(i+counter,(i+1)+counter)
            graphNode['from'] = fromNode
            graphNode['to'] = toNode
            #graphNode['edge']= nodesEdge
            graphNode['dist']=dist
            self.entityService.addDocument("graph1", graphNode)
            graphNode1 = {}
            graphNode1['index']=((i+1)+counter,i+counter)
            graphNode1['from'] = toNode
            graphNode1['to'] = fromNode
            graphNode1['dist']=dist
            self.entityService.addDocument("graph1", graphNode1)
        #return len(nodes)
    def findMinEdgeNode(self,targetEdge,osmId,edges,counter,upper_limit):
        minDist = INFINITY
        query = {"from.osmId":{"$eq":osmId}}
        targetNodeCoords = self.entityService.getDocument("graph2", query)['from']
        #print(targetNodeCoords)
        minFirstNodeCoords = None
        nodesCount = 0
        for i in range(0,upper_limit):            
            if targetEdge == i:
                nodesCount += len(edges[i]['nodes'])
                continue
            firstNode = edges[i]['nodes'][0]
            #print (firstNode)
            query={"from.osmId":{"$eq":firstNode}}
           
            if firstNode!=osmId:
                firstNodeCoords = self.entityService.getDocument("graph2",query)["from"]
                dist = Haversian.getInstance().calculateDistance(Coordinates(firstNodeCoords['lng'],firstNodeCoords['lat']),Coordinates(targetNodeCoords['lng'],targetNodeCoords['lat']))
                if dist < minDist:
                    minDist = dist
                    minFirstNodeCoords= firstNodeCoords
                    index = nodesCount 
            nodesCount += len(edges[i]['nodes'])
        #print (minDist)
        graphNode = {}
        graphNode['index']=(counter-1,index)
        graphNode['from'] = targetNodeCoords
        graphNode['to'] = minFirstNodeCoords
        #graphNode['edge']= nodesEdge
        graphNode['dist']=minDist 
        #print (graphNode)
        self.entityService.addDocument("graph2", graphNode)
        graphNode = {}
        graphNode['index']=(index,counter-1)
        graphNode['from'] = minFirstNodeCoords
        graphNode['to'] = targetNodeCoords
        graphNode['dist']=minDist
        #print (graphNode)
        self.entityService.addDocument("graph2", graphNode)
def tester():
    edgeBaseGraph = EdgeBasedGraph()
    edgeBaseGraph.parseEdgesForConnectivity()                
tester()    