'''
Created on Feb 22, 2014

@author: Devon Arrington
'''


class ProcessState(object):
    UNINITIALIZED = 0
    REMOVED = 1
    RUNNING = 2
    PAUSED = 3
    SUCCEEDED = 4
    FAILED = 5
    ABORTED = 6
    

class Process(object):
    def __init__(self):
        self.state = ProcessState.UNINITIALIZED
        self.child = None
    
    def init(self):
        self.state = ProcessState.RUNNING
    
    def update(self, time):
        pass
    
    def onSuccess(self):
        pass
    
    def onFail(self):
        pass
    
    def onAbort(self):
        pass
    
    def succeed(self):
        assert(self.state == ProcessState.RUNNING or self.state == ProcessState.PAUSED)
        self.state = ProcessState.SUCCEEDED
    
    def fail(self):
        assert(self.state == ProcessState.RUNNING or self.state == ProcessState.PAUSED)
        self.state = ProcessState.FAILED
    
    def pause(self):
        assert(self.state == ProcessState.RUNNING)
        self.state = ProcessState.PAUSED
    
    def resume(self):
        assert(self.state == ProcessState.PAUSED)
        self.state = ProcessState.RUNNING
    
    def addChild(self, child):
        if self.child:
            self.child.addChild(child)
        else:
            self.child = child
    
    def removeChild(self):
        if self.child:
            self.child = None
    
    def isRunning(self):
        return self.state == ProcessState.RUNNING or self.state == ProcessState.PAUSED
        
    def isFinished(self):
        return self.state == ProcessState.SUCCEEDED or self.state == ProcessState.FAILED or self.state == ProcessState.ABORTED
        
    
    
    
    