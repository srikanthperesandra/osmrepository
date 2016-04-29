'''
Created on Apr 4, 2016

@author: srikanth
'''
from services.entitiy.EntityService import EntityService
from pfinder.PFinderConfig import INFINITY
'''
Created on Mar 27, 2016

@author: srikanth
'''
from services.GraphEntityService import GraphEntityService
import math
from collections import deque
class ShortestFSP(object):
    def __init__(self,src,dest):
        self.graph = {}
        self.graphService = GraphEntityService()
        self.src = src
        self.dest = dest
        self.entityService = EntityService()
    def readGraph(self):
        self.graph = self.graphService.getGraph()
    def processGraph(self):
        queue = deque([])
        #numEdges = 100#int(math.sqrt(self.graph.count()))
        #nodes_edges = 300
        #dist = [float(99999000)]*(numEdges*nodes_edges)
        #srcNode =  self.entityService.getDocument("graph2",{"from.osmId":{"$eq":self.src}})#self.graphService.getNodebyOSMId(self.src)
        #destNode = self.entityService.getDocument("graph2",{"from.osmId":{"$eq":self.dest}})#self.graphService.getNodebyOSMId(self.dest)
        srcNode =  self.entityService.getDocument("cRoutes",{"from":{"$eq":self.src}})#self.graphService.getNodebyOSMId(self.src)
        destNode = self.entityService.getDocument("cRoutes",{"from":{"$eq":self.dest}})#self.graphService.getNodebyOSMId(self.dest)
        #distance from src node to itself is zero
        #print (srcNode)
        #print (destNode)
        #dist[int(srcNode['index'][0])] = 0
        visited = {}
        dist = {}
        #dist[srcNode['from']['osmId']] = 0
        # Enqueue src Node
        queue.append(srcNode)
        prev={}#[None]*(numEdges*nodes_edges)
        while len(queue) != 0:
            #print (queue)
            u = queue.popleft()
            uOsmId = u['from']
            #print (uOsmId)
            if uOsmId == destNode['from']:
                print ("reached")
                #print (dist[destNode['index'][0]])
                #return
                break
            #print(self.graphService.getNodeEdges(u['from']).count())
            for edge in self.entityService.getDocuments("cRoutes",{"from":{"$eq":uOsmId}}):#self.graphService.getNodeEdges(u['from']):
                #print (edge)
                toOsmId = edge['to']
                #print (toOsmId)
                #if not(toOsmId in dist):
                    #dist[toOsmId] = INFINITY
                #temp = dist[uOsmId]+edge['dist']
                #print (temp)
                '''dist[int(edge['index'][1])]'''
                if (not(toOsmId in visited) or (visited[toOsmId]==False or visited[toOsmId]== None)):
                    #dist[int(edge['index'][1])] = temp
                    #prev[int(edge['index'][1])] = u
                    #dist[toOsmId] = temp
                    prev[toOsmId] = uOsmId
                    visited[toOsmId] = True
                    #if not(any(obj['to']['osmId']== edge['to']['osmId'] for obj in queue)):
                        #print (edge['index'][1])
                    queue.append(self.entityService.getDocument("cRoutes",{"from":{"$eq":edge['to']}}))
                    
        
        # Stack with shortest path
        #print (dist)
        #print (prev)
        
        
        path = []
        if self.src == self.dest:
            path.append(self.src)
        else:
            x = self.dest
            path.append(x)
            while prev[x]!=self.src:
                path.append(prev[x])
                x= prev[x]
            path.append(prev[x])
        
        result = {}
        result['shortest_path']=path
        #print (result)
        #result ['distance']=dist[self.dest]
        #print (result)
        return result
    def calculateDistance(self,result):
           routes = result['shortest_path']
'''           
def tester():
    #fsp = ShortestFSP(3201068,498348)
    #tester 1
    #fsp = ShortestFSP(16463077,3413905080)
    #fsp = ShortestFSP(16463077, 27549571)
    #fsp = ShortestFSP(1749701272, 15254831)
    #fsp = ShortestFSP(295587707, 135728912)
    #fsp = ShortestFSP(5331192, 5255208)
    fsp = ShortestFSP(5331192, 5331192)
    #fsp.readGraph()
    fsp.processGraph()
tester() 
'''