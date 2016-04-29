'''
Created on Mar 23, 2016

@author: srikanth
'''
class Coordinates(object):
    def __init__(self,latitude,longitude):
        self.lat = latitude
        self.lng = longitude
    def getLatitude(self):
        return self.lat
    def getLongitude(self):
        return self.lng