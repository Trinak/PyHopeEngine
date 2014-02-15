'''
Created on Jul 24, 2013

@author: Devon

Defines class to manage game actors
'''


class ActorManager(object):
    '''Manages actors within game. Meant to be subclassed
    for game specific logic'''
    
    def __init__(self):
        self.actorDict = {}
        self.actorFactory = None
    
    def addActor(self, actor):
        self.actorDict[actor.actorID] = actor
    
    def destroyActor(self, actorID):
        actor = self.findActor(actorID)
        actor.cleanUp()
        del self.actorDict[actorID]
    
    def findActor(self, actorID):
        return self.actorDict[actorID]
    
    def createActor(self, resource, initialPos = None, actorID = None, parent = None):
        actor = self.actorFactory.createActor(resource, initialPos, actorID, parent)
        self.addActor(actor)
        
        return actor
    
    def update(self):
        for actor in self.actorDict.values():
            actor.update()
    
    def cleanUp(self):
        for actor in self.actorDict.values():
            actor.cleanUp()
            
        self.actorDict.clear()
        self.actorFactory.lastActorID = 0
        
    
    