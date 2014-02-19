'''
Created on Nov 21, 2013

@author: Devon Arrington

Defines component to hold child actors 
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine.actors.components.actorComponent import ActorComponent


class ChildActorsComponent(ActorComponent):
    '''Holds actors attached to a parent actor'''
    
    def __init__(self):
        self.name = "ChildActorsComponent"
        self.owner = None
        self.childActors = []
        self.resources = []
        
    def update(self):
        for actor in self.childActors:
            actor.update()
    
    def init(self, element):
        '''Gets each child actors XML resource'''
        for child in element:
            self.resources.append(child.text)
        
    def postInit(self):
        '''Create and add each child actor'''
        for resource in self.resources:
            actor = ECOM.actorManager.createActor(resource, parent = self.owner)
            self.childActors.append(actor)
    
    def cleanUp(self):
        for actor in self.childActors:
            actor.cleanUp()