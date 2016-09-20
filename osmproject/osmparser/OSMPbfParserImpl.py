'''
Created on Feb 9, 2016

@author: srikanth
'''
from osmparser.IOSMPbfParser import IOSMPbfParser
from imposm.parser import OSMParser
from datastructure.Graph import Graph
from datastructure.Node import Node
from datastructure.Point import Point
from datastructure.Edge import Edge
from datastructure.util.HaversianCalculator import Haversian
from datastructure.Street import Street
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
        nodes = Graph.getInstance().getNodes().keys()
        nodes_all = Graph.getInstance().getNodes()
        for osmId, meta_data,refs in ways_tuple:
            refs_set =set(refs)
            #print ('Refs who are nodes')
            common_nodes=list(refs_set.intersection(nodes))
            if len(common_nodes)>1:
                street_edges = []
                for i in range(0,len(common_nodes)-1):
                    edge = Edge(Haversian.getInstance().calculateDistance(nodes_all[common_nodes[i]].getCoords(),nodes_all[common_nodes[i+1]].getCoords()),common_nodes[i],common_nodes[i+1])
                    #print('Haversian distance from '+str(common_nodes[i])+", "+str(common_nodes[i+1]))
                    #print(edge.getDistance())
                    street_edges.append(edge)
                Graph.getInstance().addStreet(osmId, Street(osmId,meta_data,street_edges))
        
    def fetchCoords(self,coords_tuple):
        graph=Graph.getInstance()
        for osmId,lng,lat in coords_tuple:
            graph.addPoint(osmId, Point(lng,lat))
