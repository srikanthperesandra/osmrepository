'''
Created on Feb 9, 2016

@author: srikanth
'''
from osmparser.IOSMPbfParser import IOSMPbfParser
from osmparser.OSMPbfParserImpl import OSMPbfParserImpl 
from sys import argv   
from datastructure.Graph import Graph
osmPbfFile = '/home/srikanth/Msc/Sem3/bdb/workspace/osmproject/stuttgart-regbez-latest.osm.pbf'
def invokeParser():
    try:
        osmParser  = OSMPbfParserImpl(IOSMPbfParser(),osmPbfFile)#callback_type=argv[1])
        osmParser.start()
    except Exception as e:
        print(e)
def entryPoint():
    invokeParser()
    print ("Number of Nodes")
    nodes = Graph.getInstance().getNodes()
    for osmid in nodes:
        print (nodes[osmid].getMetadata())
        
entryPoint()