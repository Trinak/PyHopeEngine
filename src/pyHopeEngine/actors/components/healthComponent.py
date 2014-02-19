'''
Created on Oct 30, 2013

@author: Devon Arrington
'''

from pyHopeEngine import engineCommon as ECOM
from pyHopeEngine import Event_RequestDestroyActor
from pyHopeEngine.actors.components.actorComponent import ActorComponent


class HealthComponent(ActorComponent):
    def __init__(self):
        self.name = "HealthComponent"
        self.health = None
    
    def init(self, element):
        healthElement = element.find("Health")
        if healthElement is not None:
            self.health = eval(healthElement.text)
        else:
            self.health = 0
    
    def postInit(self):
        pass
    
    def takeDamage(self, damage):
        self.health -= damage
        
        if self.health <= 0:
            event = Event_RequestDestroyActor(self.owner.actorID)
            ECOM.eventManager.queueEvent(event)