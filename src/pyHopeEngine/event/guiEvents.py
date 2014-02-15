'''
Created on Aug 27, 2013

@author: Devon

Define gui events
'''

from pyHopeEngine import BaseEvent

class Event_ButtonPressed(BaseEvent):
    '''Sent when a button is pressed'''
    eventType = "ButtonPressed"
    
    def __init__(self, value):
        '''Contains a value identifying the button'''
        self.value = value


class Event_ScreenResize(BaseEvent):
    '''Sent when a screen resize is requestsed'''
    eventType = "ScreenResize"
    
    def __init__(self, width, height):
        self.width = width
        self.height = height