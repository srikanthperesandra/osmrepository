'''
Created on Feb 9, 2016

@author: srikanth
'''
from osmparser.IOSMPbfParser import IOSMPbfParser
from osmparser.OSMPbfParserImpl import OSMPbfParserImpl 
from pfinder.PFinderConfig import osmPbfFile
from repository.RepositoryConnection import RepositoryConnection
from pfinder.PFinderConfig import dbHost
from pfinder.PFinderConfig import dbPort
from pfinder.PFinderConfig import dbRepository
from sys import argv   
def invokeParser():
    try:
        repository=RepositoryConnection(dbHost, dbPort, dbRepository)
        osmParser  = OSMPbfParserImpl(IOSMPbfParser(),osmPbfFile,callback_type=argv[1],repository=repository)
        osmParser.start()
    except Exception as e:
        print(e)
invokeParser()
