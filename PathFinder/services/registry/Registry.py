'''
Created on Apr 10, 2016

@author: srikanth
'''
from services.entitiy.NodeService import NodeService
from fsp.ClusterGraphEntityService import ClusterGraphEntityService
from fsp.FSPService import FSPService
from services.utility.GraphHopperService import GraphHopperService
from services.entitiy.EntityService import EntityService
from fsp2.CRoutesService import CRoutesService
from services.registry.RegistryServices import RegistryServices 
class Registry(object):
    _registryInstance = None
    def __init__(self):
        self.registry = {}
        self.registry[RegistryServices.NODES_SERVICE]=NodeService()
        self.registry[RegistryServices.CGRAPH_SERVICE]=ClusterGraphEntityService()
        self.registry[RegistryServices.FSP_SERVICE]=FSPService()
        self.registry[RegistryServices.GHOPER_SERVICE]=GraphHopperService()
        self.registry[RegistryServices.ENTITY_SERVICE]=  EntityService()
        self.registry[RegistryServices.CROUTES_SERVICE]=  CRoutesService()
    @staticmethod
    def getInstance():
        if __class__._registryInstance == None:
            __class__._registryInstance = Registry()
        return __class__._registryInstance
    def getService(self,name):
        if not(name in self.registry):
            raise KeyError(name," service not found")
        return self.registry[name]
'''def tester():
    try:
        reg = Registry.getInstance().getService('node_service')
    except KeyError as e:
        print (e)
        
tester()
'''