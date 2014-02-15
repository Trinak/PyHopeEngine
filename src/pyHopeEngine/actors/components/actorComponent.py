'''
Created on Jun 21, 2013

@author: Devon

Base actor component
'''

class ActorComponent(object):    
    def __init__(self):
        self.name = "ActorComponent"
        self.owner = None
    
    def update(self):
        pass
    
    def init(self, element):
        raise NotImplementedError(self.name + ": init not implemented.")
    
    def postInit(self):
        raise NotImplementedError(self.name + ": postInit not implemented.")
    
    def cleanUp(self):
        pass