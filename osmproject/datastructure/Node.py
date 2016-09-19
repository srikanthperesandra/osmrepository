'''
Created on Sep 6, 2016

@author: srikanth
'''
from datastructure.Point import Point
class Node(object):
    def __init__(self,osmid,metadata,coords):
        self.metadata = metadata
        self.coords = Point(coords[0],coords[1])
        self.osmid=osmid
    def getName(self):
        return self.name
    def getMetadata(self):
        return self.metadata
    def getCoords(self):
        return self.coords
    def getOSMId(self):
        return self.osmid