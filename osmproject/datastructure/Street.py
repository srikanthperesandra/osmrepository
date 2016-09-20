'''
Created on Sep 20, 2016

@author: srikanth
'''
class Street(object):
    def __init__(self,osmId,metadata,edges):
        self.osmId = osmId
        self.metadata = metadata
        self.edges = edges
    def getMetadata(self):
        return self.metadata
    def getEdges(self):
        return self.edges
