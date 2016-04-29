'''
Created on Feb 9, 2016

@author: srikanth
'''
osmPbfFile = "/home/srikanth/Msc/Sem3/OSM/workspace/PathFinder/dataSoruce/BW.osm.pbf"
dbHost = "localhost"
dbPort = 27017
dbRepository="pFinderDB"

#dbWaysCollection = "ways1"
#dbNodesCollection = "nodes"
dbNodesCollection = "nodes2"
dbWaysCollection = "ways2"
#dbRelationsCollection = "relations"
dbRelationsCollection = "relations1" 
dbGraph = "graph"
dbCoordsCollection = "coords"
dbFSPResult = "fspResult"
dbCRoute = "cRoutes"
dbCRoutesStreet = "cRoutesStreets"
#dbClusterGraph = "cGraph"
#dbClusterEdges = "cEdges"
dbClusterGraph = "cGraph_V1"
dbClusterEdges = "cEdges_V1"
dbGraphHoper_url = "www.graphhopper.com"
dbGrapherHoper_key = "2c9f274a-b7a1-4bb5-9893-19f8712f9a16"
INFINITY = float(99999000)