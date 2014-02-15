'''
Created on Oct 15, 2013

@author: Devon Arrington
'''

from pyHopeEngine import BaseEvent


class Event_PlayAnimation(BaseEvent):
    '''Request an animation be set to play'''
    eventType = "PlayAnimation"
    
    def __init__(self, actorID, name):
        '''Contains a name identifying the animation'''
        self.actorID = actorID
        self.name = name
