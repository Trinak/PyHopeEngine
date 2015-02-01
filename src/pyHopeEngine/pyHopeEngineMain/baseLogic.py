'''
Created on May 31, 2013

@author: Devon

Defines the base logic of the engine
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import PhysicsManager, NullPhysics
from pyHopeEngine import ProcessManager
from pyHopeEngine import Event_ActorMoved, Event_SetRemoteActor, Event_CreateNewActor, Event_SetControlledActor, Event_RequestDestroyActor, Event_DestroyActor
from pyHopeEngine import NetworkEventForwarder

class BaseLogic(object):
    '''Base logic of game'''
    
    def __init__(self):
        self.processManager = ProcessManager()
        self.physics = PhysicsManager()
        self.gameStates = []
        self.gameViewList = []
        self.actorManager = None
        self.proxy = False
        self.networkEventForwarder = None
    
    def init(self):
        '''Initialize the game logic'''
        ECOM.eventManager.addListener(self.destroyActor, Event_RequestDestroyActor.eventType)
    
    def addView(self, gameView):
        '''Add a game view'''
        self.gameViewList.append(gameView)
    
    def removeView(self, gameView):
        '''Remove a game view'''
        self.gameViewList.remove(gameView)
    
    def addProcess(self, process):
        if self.processManager is not None:
            self.processManager.addProcess(process)
            
    def createActor(self, resource, initialPos = None, actorID = None, parent = None):
        '''Create an actor from the given resource'''
        actor = self.actorManager.createActor(resource, initialPos, actorID, parent)
        
        if not self.proxy:
            event = Event_CreateNewActor(resource, actor.actorID)
            ECOM.eventManager.triggerEvent(event)
        
        return actor
    
    def findActor(self, actorID):
        '''Find an actor based on the ID'''
        actor = self.actorManager.findActor(actorID)
        return actor
    
    def update(self, elapsedTime):
        '''Update the various game systems'''
        self.processManager.update(elapsedTime)
        self.gameStates[-1].update(self)
        
        for view in self.gameViewList:
            view.update()
        
        self.physics.update(1.0/60.0)
        self.physics.syncWithGraphics()
        
        self.actorManager.update()

    def changeState(self, state):
        '''Changes the game state'''
        if self.gameStates:
            self.gameStates[-1].cleanUp(self)
            self.gameStates.pop()
        
        self.gameStates.append(state)
        self.gameStates[-1].init(self)
    
    def setProxy(self):
        '''Turns the logic into a proxy logic'''
        self.proxy = True
        self.physics = NullPhysics()
        
        eventManager = ECOM.eventManager
        eventManager.addListener(self.createNewActor, Event_CreateNewActor.eventType)
        eventManager.addListener(self.setRemoteActor, Event_SetRemoteActor.eventType)
    
    def createNewActor(self, event):
        '''Handle create actor event from server'''
        self.createActor(event.resource, event.actorID)
    
    def setRemoteActor(self, event):
        '''Server creates event to set a clients actor'''
        event = Event_SetControlledActor(event.actorID)
        ECOM.eventManager.triggerEvent(event)
    
    def destroyActor(self, event):
        '''Destroys an actor'''
        self.actorManager.destroyActor(event.actorID)
        event = Event_DestroyActor(event.actorID)
        ECOM.eventManager.triggerEvent(event)
    
    def createNetworkEventForwarder(self):
        '''Create an event forwarder for server and client to communicate'''
        self.networkEventForwarder = NetworkEventForwarder(ECOM.engine.networkManager)
        
        eventManager = ECOM.eventManager
        if not self.proxy:
            eventManager.addListener(self.networkEventForwarder.forwardEvent, Event_ActorMoved.eventType)
            eventManager.addListener(self.networkEventForwarder.forwardEvent, Event_SetRemoteActor.eventType)
            eventManager.addListener(self.networkEventForwarder.forwardEvent, Event_CreateNewActor.eventType)
    
    def addPhysicsConstraint(self, constraintType, actorIDA, actorIDB, **kwargs):
        '''Add a contraint between two actors'''
        self.physics.addConstraint(constraintType, actorIDA, actorIDB, **kwargs)