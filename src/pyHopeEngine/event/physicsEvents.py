'''
Created on Aug 27, 2013

@author: Devon

Defines physics events
'''

from pyHopeEngine import BaseEvent

class Event_ChangeVelocity(BaseEvent):
    '''Sent when requesting a velocity change'''
    eventType = "ChangeVelocity"
    
    def __init__(self, actorID, velocity):
        self.actorID = actorID
        self.velocity = velocity


class Event_ChangeAngularVelocity(BaseEvent):
    '''Sent when requesting a change in an actors angular velocity'''
    eventType = "ChangeAngularVelocity"
    
    def __init__(self, actorID, velocity):
        self.actorID = actorID
        self.angularVelocity = velocity
        

class Event_ApplyForce(BaseEvent):
    '''Sent when requesting a force applied to actor'''
    eventType = "ApplyForce"
    
    def __init__(self, actorID, magnitude, offset = (0, 0)):
        self.actorID = actorID
        self.magnitude = magnitude
        self.offset = offset


class Event_ApplyImpulse(BaseEvent):
    '''Sent when requesting an impulse applied to actor'''
    eventType = "ApplyImpulse"
    
    def __init__(self, actorID, direction, magnitude, offset = (0, 0)):
        self.actorID = actorID
        self.direction = direction
        self.magnitude = magnitude
        self.offset = offset


class Event_Accelerate(BaseEvent):
    '''Sent went requesting actor to accelerate'''
    eventType = "Accelerate"
    
    def __init__(self, actorID, magnitude):
        self.actorID = actorID
        self.magnitude = magnitude


class Event_Decelerate(BaseEvent):
    '''Sent when requesting actor to decelerate'''
    eventType = "Decelerate"
    
    def __init__(self, actorID, magnitude):
        self.actorID = actorID
        self.magnitude = magnitude

