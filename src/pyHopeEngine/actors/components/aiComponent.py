'''
Created on Jul 27, 2013

@author: Devon

Defines base AI component
'''

from pyHopeEngine.actors.components.actorComponent import ActorComponent

class AIComponent(ActorComponent):
    '''Base AI component'''
    
    def __init__(self):
        self.owner = None
        self.name = "AIComponent"