'''
Created on Apr 11, 2016

@author: srikanth
'''
from pfinder.PFinderConfig import dbGraphHoper_url, dbGrapherHoper_key
from http.client import HTTPConnection, HTTPSConnection
from fsp.Coordinates import Coordinates
class GraphHopperService(object):
    def __init__(self):
        self.url = None
    def invokeRoutingService(self,point1,point2):
        self.url = dbGraphHoper_url
        self.url_path = "/api/1/route"+"?point="+str(point1.getLatitude())+","+str(point1.getLongitude())+"&point="+str(point2.getLatitude())+","+str(point2.getLongitude())+"&vehicle=foot"+"&key="+dbGrapherHoper_key+"&type=json&points_encoded=false"
        print (self.url_path)
        http = HTTPSConnection(self.url)
        http.request("GET", self.url_path)
        response = http.getresponse()
        data= response.read()
        response.close()
        return data
    def processResult(self,result):
        print (result)

'''def tester():
    point1 = Coordinates(49.006165999999986,8.326746199999988)
    point2 = Coordinates(49.008863200000285,8.405402699999954)
    gph_service = GraphHopperService()
    gph_service.invokeRoutingService(point1, point2)
tester()
'''    