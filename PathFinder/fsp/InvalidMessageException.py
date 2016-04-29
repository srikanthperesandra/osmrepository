'''
Created on Apr 9, 2016

@author: srikanth
'''
class InvalidMessageException(object):
    def __init__(self,message):
      self.mesg = message
    def __str__(self):
        return self.mesg
'''def tester():
    e = InvalidMessageException("message")
    print (e)
tester()
'''