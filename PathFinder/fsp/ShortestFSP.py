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
    def readGraph(self):
        self.graph = self.graphService.getGraph()
    def processGraph(self):
        queue = deque([])
        numNodes = int(math.sqrt(self.graph.count()))
        dist = [float(99999000)]*numNodes
        srcNode =  self.graphService.getNodebyOSMId(self.src)
        destNode = self.graphService.getNodebyOSMId(self.dest)
        #distance from src node to itself is zero
        print (srcNode)
        print (destNode)
        dist[srcNode['index'][0]] = 0
        # Enqueue src Node
        queue.append(srcNode)
        prev=[None]*numNodes
        while len(queue) != 0:
            print (queue)
            u = queue.popleft()
            if u['from'] == destNode['from']:
                print ("reached")
                print (dist[destNode['index'][0]])
                return
            #print(self.graphService.getNodeEdges(u['from']).count())
            for edge in self.graphService.getNodeEdges(u['from']):
                temp = dist[u['index'][0]]+edge['distance']
                #print (temp)
                if  temp < dist[edge['index'][1]]:
                    dist[edge['index'][1]] = temp
                    prev[edge['index'][1]] = u
                    if not(any(obj['index'][1]== edge['index'][1] for obj in queue)):
                        #print (edge['index'][1])
                        queue.append(self.graphService.getNodebyOSMId(edge['to']))
                        
                    
        
        # Stack with shortest path
        shortestPath = []
        u = destNode['index'][0]
        
        while prev[u]!=None:
            shortestPath.append(u)
            u = prev[u]['index'][0]
        shortestPath.append(u)
        print (len(shortestPath))
        #self.dist[]
    def __min__(self,dist):
        min = dist[0]
        index = 0
        for i in range(1,len(dist)):
            if dist[i] < min:
                min = dist[i]
                index = i
        return index    
def tester():
    fsp = ShortestFSP(3201068,498348)
    fsp.readGraph()
    fsp.processGraph()
tester() 