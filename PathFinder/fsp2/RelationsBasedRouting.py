'''
Created on Apr 16, 2016

@author: srikanth
'''
from fsp2.PFinderConfig import dbRelationsCollection, dbCRoute, dbCRoutesStreet
from services.entitiy.EntityService import EntityService
from services.registry.Registry import Registry
from services.entitiy.CoordsService import CoordsService
import fsp2
class RelationsBasedRouting(object):
    def __init__(self):
        #print ('reached constructor')
        self.entity_service = EntityService()
    def connectRoutes(self):
        MAX_BUCKET_SIZE = 500
        bucket = []
        pedestrian_routes = self.entity_service.getAllDocuments(dbRelationsCollection)
        for i in range(0,pedestrian_routes.count()):
            src = pedestrian_routes[i]
            print (src['osmId'])
            src_ways = set(pedestrian_routes[i]['refs'])
            for j in range(0,pedestrian_routes.count()):
                if pedestrian_routes[j]['osmId']!=pedestrian_routes[i]['osmId']:
                    common_nodes = list(src_ways.intersection(pedestrian_routes[j]['refs']))
                    if(len(common_nodes)>0):
                        result={}
                        result['from'] = src['osmId']
                        result['to'] = pedestrian_routes[j]['osmId']
                        result['commonNodes'] = common_nodes
                       
                        if len(bucket) == MAX_BUCKET_SIZE:    
                            self.entity_service.addDocuments(dbCRoute, bucket)
                            print ("bulk update of "+str(MAX_BUCKET_SIZE)+" is completed")
                            del bucket[:]
                        #print (bucket)
                        bucket.append(result)
                    #else:
                        #print ("common streets not found between "+str(src["osmId"])+" and "+str(pedestrian_routes[j]['osmId']))
        if len(bucket)>0:
            self.entity_service.addDocuments(dbCRoute, bucket)
            print ("Residual bulk update in progress")
            del bucket[:] 
    def addDistinctStreets(self):
        #print ('here')
        cRouteService = Registry.getInstance().getService("cRoutes_service")
        #print ("reached")
        streets=cRouteService.getDistinctStreets()
        #print (streets)
        coords_service = CoordsService()
        ways_collection = fsp2.PFinderConfig.dbWaysCollection
        for street in streets:
            target_street = self.entity_service.getDocument(ways_collection, {'osmId':street})
            if target_street== None:
                continue
            result = {}
            result['targetNode'] = coords_service.getCoordinate(target_street['nodes'][0]) 
            result['street'] = target_street
            #print (result)
            self.entity_service.addDocument(dbCRoutesStreet, result)
def tester():
    rb = RelationsBasedRouting()
    rb.addDistinctStreets()
tester()          