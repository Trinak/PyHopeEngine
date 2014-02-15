'''
Created on Jul 16, 2013

@author: Devon

Defines base game state
'''

class BaseState(object):
    '''Base game state'''
    def __init__(self):
        pass
    
    
    def init(self, logic):
        raise NotImplementedError("init not implemented.")
        
    
    def cleanUp(self, logic):
        raise NotImplementedError("cleanUp not implemented.")
    
    
    def update(self, logic):
        raise NotImplementedError("update not implemented.")