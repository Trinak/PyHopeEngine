'''
Created on Aug 27, 2013

@author: Devon

Defines network events
'''

from pyHopeEngine import BaseEvent

class Event_ClientConnected(BaseEvent):
    '''Sent when a client connects to server'''
    eventType = "ClientConnected"
    
    def __init__(self):
        pass


class Event_IPInput(BaseEvent):
    '''Sent to validate an IP address user inputs'''
    eventType = "IPInput"
    
    def __init__(self, ip):
        self.ip = ip
        

class Event_IPValid(BaseEvent):
    '''Sent when the IP address is a valid one'''
    eventType = "IPValid"
    
    def __init__(self, isValid):
        self.isValid = isValid