'''
Created on Sep 6, 2016

@author: srikanth
'''
class Graph(object):
    _gInstance = None
    def __init__(self):
        self.nodes ={}
        self.streets={}
        self.coords={}
    def addNode(self,osmid,node):
        self.nodes[osmid] = node
    def getNodes(self):
        return self.nodes
    def addPoint(self,osmId,point):
        self.coords[osmId]=point
    def getPoints(self):
        return self.coords
    def addStreet(self,streetId,street):
        self.streets[streetId] = street
    @staticmethod
    def getInstance():
        if __class__._gInstance == None:
            __class__._gInstance = Graph()
        return __class__._gInstance