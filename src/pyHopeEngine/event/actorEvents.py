'''
Created on Aug 27, 2013

@author: Devon

Defines actor events
'''

from pyHopeEngine import BaseEvent

class Event_CreateNewActor(BaseEvent):
    '''Sent when requesting an actor be created'''
    eventType = "CreateNewActor"
    
    def __init__(self, resource, initialPos, actorID = None, viewID = None):
        '''Creates a created actor event. 
        
        Keyword arguments:
            resource -- actors XML file
            actorID -- actors ID
            viewID -- view ID if actor is associated with a view
        '''
            
        self.resource = resource
        self.initialPos = initialPos
        self.actorID = actorID
        self.viewID = viewID
        

class Event_NewRenderComponent(BaseEvent):
    '''Sent when render component created'''
    eventType = "NewRenderComponent"
    
    def __init__(self, actorID, sceneNode, toParent = False):
        '''Creates a new render component event.
        
        Keyword arguments:
            actorID -- actor ID of the owning actor
            sceneNode -- the scene node created by the component
            toParent -- indicates if the node is a child to an existing node
        '''
        self.actorID = actorID
        self.sceneNode = sceneNode
        self.toParent = toParent


class Event_ActorMoved(BaseEvent):
    '''Sent when an actor is moved'''
    eventType = "ActorMoved"
    
    def __init__(self, actorID, pos, angle):
        self.actorID = actorID
        self.pos = pos
        self.angle = angle


class Event_SetControlledActor(BaseEvent):
    '''Sent to set a views controlled actor'''
    eventType = "SetControlledActor"
    
    def __init__(self, actorID):
        self.actorID = actorID


class Event_SetRemoteActor(BaseEvent):
    '''Sent to remote players to set their controlled actor'''
    eventType = "SetRemoteActor"
    
    def __init__(self, actorID):
        self.actorID = actorID


class Event_ActorDestroyed(BaseEvent):
    '''Sent when an actor is destroyed'''
    eventType = "ActorDestroyed"
    
    def __init__(self, actorID):
        self.actorID = actorID


class Event_RequestDestroyActor(BaseEvent):
    '''Sent when requesting an actor be destroyed'''
    eventType = "RequestDestroyActor"
    
    def __init__(self, actorID):
        self.actorID = actorID


