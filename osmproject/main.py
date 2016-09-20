'''
Created on Sep 20, 2016

@author: srikanth
'''
from osmparser.ParseOSMPbf import invokeParser
from datastructure.Graph import Graph
def entryPoint():
    invokeParser('nodes_callback')
    #keys = Graph.getInstance().getNodes().keys()
    invokeParser('ways_callback')
entryPoint()