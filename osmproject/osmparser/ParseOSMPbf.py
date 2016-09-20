'''
Created on Feb 9, 2016

@author: srikanth
'''
from osmparser.IOSMPbfParser import IOSMPbfParser
from osmparser.OSMPbfParserImpl import OSMPbfParserImpl 
from sys import argv   
from datastructure.Graph import Graph
osmPbfFile = '/home/srikanth/git/osmrepositoryV1/osmproject/stuttgart-regbez-latest.osm.pbf'
def invokeParser(callback_type):
    osmParser  = OSMPbfParserImpl(IOSMPbfParser(),osmPbfFile,callback_type=callback_type)
    osmParser.start()