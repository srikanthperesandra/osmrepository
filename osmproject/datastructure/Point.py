'''
Created on Sep 6, 2016

@author: srikanth
'''
class Point(object):
    def __init__(self,lng,lat):
        self.lng=lng
        self.lat=lat
    def getLat(self):
        return self.lat
    def getLng(self):
        return self.lng 