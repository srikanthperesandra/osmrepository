'''
Created on Apr 18, 2016

@author: srikanth
'''
from fsp2.PFinderConfig import dbCRoute
from fsp2.PFinderConfig import dbRelationsCollection
#from services.registry.Registry import Registry
from fsp2.PFinderConfig import dbCRoutesStreet
from operator import itemgetter
from services.entitiy.EntityService import EntityService
from collections import OrderedDict
class CRoutesService(object):
    def __init__(self):
        self.cRoutesCollection = dbCRoute
        self.relationsCollection = dbRelationsCollection
        self.entityService = EntityService()#Registry.getInstance().getService("entity_service")
    def getDistinctRoutes(self):
        return self.entityService.getDistinctDocuments(self.cRoutesCollection,"from")
    def getDistinctStreets(self):
        return self.entityService.getDistinctDocuments(self.cRoutesCollection,"commonNodes")
    def getCommonStreetsBetweenRoutes(self,src,dest):
        query = {"from":src,"to":dest}
        return self.entityService.getDocument(self.cRoutesCollection,query)
    def getRouteInformation(self,osmId):
        query = {'osmId':osmId}
        return self.entityService.getDocument(dbRelationsCollection, query)
    def getRoutefromStreet(self,street):
        query = {"commonNodes":{"$in":[street]}}
        return self.entityService.getDocument(self.cRoutesCollection, query)
    def getcRoutesStreets(self,query):
        attrubutes_exclusion = {"_id":0,"street.nodes":0}
        return self.entityService.getDocuments2(dbCRoutesStreet, query,attrubutes_exclusion)
    def getcRoutesStreetsWithNames(self):
        attrubutes_exclusion = {"_id":0,"street.nodes":0}
        query = {"street.meta_data.name":{"$exists":True}}
        return self.entityService.getDocuments2(dbCRoutesStreet, query,attrubutes_exclusion)
    def getRoutefromStreet2(self,street):
        command  = OrderedDict()
        command['distinct']=self.cRoutesCollection
        command['key']="from"
        command['query']={"commonNodes":{"$in":[street]}}
        return self.entityService.runCommand(command)