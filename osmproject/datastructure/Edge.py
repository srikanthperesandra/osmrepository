'''
Created on Sep 20, 2016

@author: srikanth
'''
class Edge(object):
    def __init__(self,dist,from_node, to_node):
        self.dist = dist
        self.from_node = from_node
        self.to_node = to_node
    def getDistance(self):
        return self.dist