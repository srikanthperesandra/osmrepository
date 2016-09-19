'''
Created on Feb 9, 2016

@author: srikanth
'''
from osmparser.IOSMPbfParser import IOSMPbfParser
from imposm.parser import OSMParser
from datastructure.Graph import Graph
from datastructure.Node import Node
from datastructure.Point import Point
class OSMPbfParserImpl:
    def __init__(self,interface,osmPbfFile,callback_type=None,repository=None):
        #print(IOSMPbfParser)#
        if not isinstance(interface, IOSMPbfParser): raise Exception("Bad Interface")
        self.osmPbfFile = osmPbfFile
        if(callback_type== "nodes_callback"):
            self.parser = OSMParser(concurrency=4,nodes_callback=self.fetchNodes)
            print ("Initializing Nodes Callback......")
        elif(callback_type== "ways_callback"):
            self.parser = OSMParser(concurrency=4,ways_callback=self.fetchWays)
            print ("Initializing Ways Callback......")
        elif(callback_type== "relations_callback"):
            self.parser = OSMParser(concurrency=4,relations_callback=self.fetchRelations)
            print ("Initializing Relations Callback......")
        elif(callback_type== "coords_callback"):
            self.parser = OSMParser(concurrency=4,coords_callback=self.fetchCoords)
            print ("Initializing Coords Callback......")
        else:
            self.parser = OSMParser(concurrency=4,nodes_callback=self.fetchNodes)
        self.repository= repository
    def start(self):
        print ("Started Parser.......")
        self.parser.parse(self.osmPbfFile)    
    def fetchNodes(self,nodes_tuple):
        for osmId, meta_data,coords in nodes_tuple:
            #print (osmId)
            Graph.getInstance().addNode(osmId,Node(osmId,meta_data,coords))
        #print(len(Graph.getInstance().getNodes()))
    def fetchWays(self,ways_tuple,collection=None):
        for osmId, meta_data,refs in ways_tuple:
                print (osmId)
        
    def fetchCoords(self,coords_tuple):
        graph=Graph.getInstance()
        for osmId,lng,lat in coords_tuple:
            graph.addPoint(osmId, Point(lng,lat))
