'''
Created on May 6, 2013

@author: Devon

Defines the event manager
'''

NUM_QUEUES = 2

class EventManager(object):
    '''Main event manager'''
    
    def __init__(self):
        self.eventListeners = {}
        self.eventQueues = [[] for x in range(NUM_QUEUES)]
        self.activeQueue = 0
        
    def addListener(self, listener, eventType):
        '''Adds a listener to the event manager'''
        if listener in self.eventListeners.values():
            return
        
        if eventType in self.eventListeners:
            self.eventListeners[eventType].append(listener)
        else:
            self.eventListeners[eventType] = []
            self.eventListeners[eventType].append(listener)
    
    def removeListener(self, listener, eventType):
        '''Removes a listener from the event manager'''
        if eventType in self.eventListeners:
            self.eventListeners[eventType].remove(listener)
            
            if not self.eventListeners[eventType]:
                del self.eventListeners[eventType]
        
    def queueEvent(self, event):
        '''Adds an event to the queue'''
        if event.eventType not in self.eventListeners:
            return
        
        self.eventQueues[self.activeQueue].append(event)
    
    def triggerEvent(self, event):
        '''Immediately triggers an event to be processed'''
        eventType = event.eventType
        if eventType not in self.eventListeners:
            return
        
        for handler in self.eventListeners[eventType]:
            handler(event)
    
    def cancelEvent(self, eventType, allType = False):
        '''Removes an event from the queue'''
        if eventType not in self.eventListeners:
            return
        
        eventQueue = list(self.eventQueues[self.activeQueue])
        for event in eventQueue:
            if event.eventType == type:
                self.eventQueues[self.activeQueue].remove(event)
                
                if not allType:
                    break
            
    def update(self):
        '''Handles all events in the queue'''
        eventQueue = list(self.eventQueues[self.activeQueue])
        self.eventQueues[self.activeQueue].clear()
        self.activeQueue = (self.activeQueue + 1) % NUM_QUEUES
        
        for event in eventQueue:
            eventType = event.eventType
            if eventType not in self.eventListeners:
                continue
            for handler in self.eventListeners[eventType]:
                handler(event)
                
        
            
            