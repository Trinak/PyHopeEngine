'''
Created on Jun 4, 2013

@author: Devon

Defines base actor
'''

class Actor(object):
    '''Main actor object'''
    
    def __init__(self, actorID):
        '''Creates a new actor object.
        
        Keyword arguments:
            actorID -- unique ID of the actor
        '''
        
        self.actorID = actorID
        self.components = []
        self.type = None
        self.resource = None
        self.parent = None
    
    
    def init(self, element):
        '''Initializes actor using XML element'''
        self.type = element.attrib.get("type")
        self.resource = element.attrib.get("resource")
    
    
    def addComponent(self, component):
        '''Adds a component to the actor'''
        self.components.append(component)
    
    
    def removeComponent(self, name):
        '''Removes component from actor'''
        comp = self.getComponent(name)
        comp.cleanUp()
        self.components.remove(comp)
        
    
    def getComponent(self, name):
        '''Returns a component based on its name'''
        for component in self.components:
            if component.name == name:
                return component
        
        return None
    
    
    def postInit(self):
        for component in self.components:
            component.postInit()
            
    
    def update(self):
        for component in self.components:
            component.update()
    
    
    def cleanUp(self):
        for component in self.components:
            component.cleanUp()