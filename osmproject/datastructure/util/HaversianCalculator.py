'''
Created on Mar 23, 2016

@author: srikanth
'''
import math
from datastructure.Point import Point
class Haversian(object):
    _haversian_instance = None
    def __init__(self):
        self.degree_radians = math.pi/180.0
        self.earth_mean_radius = 6371000
    @staticmethod
    def getInstance():
        if __class__._haversian_instance == None:
            __class__._haversian_instance = Haversian()
        return __class__._haversian_instance
    def calculateDistance(self,src,dest):
        phy1 = src.getLat()*self.degree_radians
        phy2 = dest.getLat()*self.degree_radians
        delta_phy = (src.getLat()-dest.getLat())*self.degree_radians
        #print (src.getLng())
        delta_theta = (src.getLng()*self.degree_radians)-(dest.getLng()*self.degree_radians)
        a = (math.sin(delta_phy/2) * math.sin(delta_phy/2)) +(math.cos(phy1) * math.cos(phy2))*(math.sin(delta_theta/2) * math.sin(delta_theta/2));
        return self.earth_mean_radius * 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        
'''def test():
    src = Point(8.326746199999988,49.006165999999986)  
    dest = Point(9.976826499999982,48.3516758)
    h = Haversian.getInstance()
    print(h.calculateDistance(src, dest))

test()
'''

  
        