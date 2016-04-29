'''
Created on Apr 9, 2016

@author: srikanth
'''
from fsp.ShortestFSP2 import ShortestFSP
from fsp.InvalidMessageException import InvalidMessageException
from copy import deepcopy
from fsp.ClusterGraphEntityService import ClusterGraphEntityService
#from services.registry.Registry import Registry
import fsp2
from fsp2.CRoutesService import CRoutesService
from fsp2.ShortestFSP2 import ShortestFSP as ShortestFSPV2
from services.entitiy.EntityService import EntityService
from services.entitiy.CoordsService import CoordsService
from fsp.HaversianCalculator import Haversian
from fsp.Coordinates import Coordinates
from fsp2.PFinderConfig import dbCRoutesStreet
class FSPService(object):
    def __init(self):
        self.fsp = None
    def calculateShortestPath(self,src,dest):
        self.fsp = ShortestFSP(src,dest)
        result = self.fsp.processGraph()
        return result
    def processResult(self,result):
        if not('distance' in result):
            raise InvalidMessageException("Invalid result from Shortest path, KeyError:'distance' not found")
        if not('shortest_path' in result):
            raise InvalidMessageException("Invalid result from Shortest path, KeyError:'shortest_path' not found")
        path = deepcopy(result['shortest_path'])
        streets = []
        clusterService = ClusterGraphEntityService()
        while len(path)>0:
            temp_path = path.pop()
            streets.append(clusterService.getStreetfromNode(temp_path))
        processed_result = {}
        processed_result['source'] = self.fsp.src
        processed_result['destination'] = self.fsp.dest
        processed_result['path'] = streets
        processed_result['distance'] = result['distance']
        return processed_result
    def processRelationBasedFSPResult(self,result,src_street,dest_street):
        if not('shortest_path' in result):
            raise InvalidMessageException("Invalid result from Shortest path, KeyError:'shortest_path' not found")
        path = deepcopy(result['shortest_path'])
        cRouteService = CRoutesService()#Registry.getInstance().getService("cRoutes_service")
        entityService = EntityService()
        coords_service = CoordsService()
        ways_collection = fsp2.PFinderConfig.dbWaysCollection
        i = len(path)-1
        final_set = set()
        sum = 0
        final_result = {}
        final_result['points'] = []
        final_result['routes']= []
        prev_point = entityService.getDocument(dbCRoutesStreet,{'street.osmId':src_street})['targetNode']
        final_result['points'].append(prev_point)
        while(i>=1):
            common_streets = cRouteService.getCommonStreetsBetweenRoutes(path[i],path[i-1])['commonNodes']
            target_street = entityService.getDocument(dbCRoutesStreet, {'street.osmId':common_streets[0]})
            if target_street== None:
                i=i-1
                continue
            point = target_street['targetNode']
            sum = sum + Haversian.getInstance().calculateDistance(Coordinates(prev_point['lng'],prev_point['lat']),Coordinates(point['lng'],point['lat']) )
            #dest = coords_service.getCoordinate(target_street['nodes'][len(target_street['nodes'])-1])
            #sum = sum+Haversian.getInstance().calculateDistance(Coordinates(src['lng'],src['lat']),Coordinates(dest['lng'],dest['lat']) )
            final_result['points'].append(point)
            #final_result['points'].append(dest)
            temp_route = cRouteService.getRouteInformation(path[i])
            final_result['routes'].append({"osmId":temp_route['osmId'],"metaData":temp_route['metaData']})
            prev_point = point
            #min_nodes = len(target_street['nodes'])
            #for j in range(1,len(common_streets)):
                #print (common_streets[i])
            #    street = entityService.getDocument(ways_collection, {'osmId':common_streets[j]})
            #   if street== None:
            #        continue
            #    if len(street['nodes'])<min_nodes:
            #        min_nodes = len(street['nodes'])
            #         target_street= street
            #print (target_street)  
            #print (common_streets) 
            i=i-1
        final_result['points'].append(entityService.getDocument(dbCRoutesStreet,{'street.osmId':dest_street})['targetNode'])
        final_result['routes'].append(cRouteService.getRouteInformation(path[0]))
        if sum==0:
            point = entityService.getDocument(dbCRoutesStreet,{'street.osmId':dest_street})['targetNode']
            sum=sum+Haversian.getInstance().calculateDistance(Coordinates(prev_point['lng'],prev_point['lat']),Coordinates(point['lng'],point['lat']) )
        final_result['distance'] = sum
        return final_result
        #print (final_result)
    def preprocessRelationBasedFSPResult(self,src_street,dest_street):
        cRouteService = CRoutesService()
        #print (src_street)
        #print (dest_street)
        from_route= cRouteService.getRoutefromStreet(src_street)['from']   
        to_route = cRouteService.getRoutefromStreet(dest_street)['from']
        return [from_route,to_route]
    def invokeRelationBasedFSPService(self,src_street,dest_street):
        routes = self.preprocessRelationBasedFSPResult(src_street, dest_street)
        fsp = ShortestFSPV2(routes[0],routes[1])
        return self.processRelationBasedFSPResult(fsp.processGraph(), src_street, dest_street)
    def preprocessRelationBasedFSPResult2(self,src_street,dest_street):
        cRouteService = CRoutesService()
        #print (src_street)
        #print (dest_street)
        from_route= cRouteService.getRoutefromStreet2(src_street)['values']   
        to_route = cRouteService.getRoutefromStreet2(dest_street)['values']
        return [from_route,to_route]
    def invokeRelationBasedFSPService2(self,src_street,dest_street):
        routes = self.preprocessRelationBasedFSPResult2(src_street, dest_street)
        src_route = routes[0][0]
        sRoutes = []
        for dest_route in routes[1]:
            fsp = ShortestFSPV2(src_route,dest_route)
            sRoutes.append(self.processRelationBasedFSPResult(fsp.processGraph(), src_street, dest_street))
        return sRoutes         
'''
def tester1():
    fsp_service = FSPService()
    #result=fsp_service.calculateShortestPath(1048707328, 295587707)
    #print (fsp_service.processResult(result))
    #fsp_service.processRelationBasedFSPResult({'shortest_path':[5255208, 3546885, 3789047, 96761, 1485435, 2127054, 1702824, 5331192]}, 0, 1)
    print (fsp_service.invokeRelationBasedFSPService2(28300224,26836034))
tester1()
'''